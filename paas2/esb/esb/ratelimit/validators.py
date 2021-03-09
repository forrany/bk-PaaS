# -*- coding: utf-8 -*-
import copy

from django.conf import settings

from lib.redis_rate_limit.ratelimit import RateLimiter
from common.base_validators import BaseValidator
from common.base_redis import redisdb
from common.errors import error_codes
from common.log import logger


RATE_LIMIT_KEY_NAMESPACE = settings.RATE_LIMIT_KEY_NAMESPACE


class ApiRateLimitValidator(BaseValidator):
    def validate(self, request):
        app_code = request.g.app_code
        comp_path = request.g.comp_path
        channel_conf = request.g.channel_conf

        if not (
            channel_conf.get("rate_limit_required")
            and channel_conf.get("rate_limit_conf")
            and channel_conf.get("id") is not None
        ):
            return

        identifier = "api::{app_code}::{component_id}".format(app_code=app_code, component_id=channel_conf["id"])
        limiter = RateLimiter(redisdb, identifier, namespace=RATE_LIMIT_KEY_NAMESPACE)

        app_rate_limit_conf = self.get_app_rate_limit_conf(app_code, channel_conf["rate_limit_conf"])
        rate_limit_message = []
        for conf in app_rate_limit_conf:
            conf = copy.deepcopy(conf)
            tokens = int(conf.pop("tokens"))
            limiter.add_rule(tokens, conf)
            rate_limit_message.extend(["%s/%s%s" % (tokens, val, key) for key, val in conf.iteritems()])

        try:
            result = limiter.acquire()
        except Exception:
            logger.exception("An exception occurred while getting rate_limit token")
            return

        if not result["allowed"]:
            raise error_codes.RATE_LIMIT_RESTRICTION.format_prompt(
                "Access frequency of APP [%s] to component [%s] exceeds the limit; the frequency limit is [%s], "
                "please try again later" % (app_code, comp_path, ";".join(rate_limit_message))
            )

    def get_app_rate_limit_conf(self, app_code, rate_limit_conf):
        app_ratelimit = rate_limit_conf["app_ratelimit"]
        return app_ratelimit.get(app_code) or app_ratelimit.get("__default", [])