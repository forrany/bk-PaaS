/**
 * Tencent is pleased to support the open source community by making 蓝鲸智云PaaS平台社区版 (BlueKing PaaS Community Edition) available.
 * Copyright (C) 2017-2019 THL A29 Limited, a Tencent company. All rights reserved.
 * Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * http://opensource.org/licenses/MIT
 * Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
 * an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
 * specific language governing permissions and limitations under the License.
 */

import grid1 from '../bk/grid/column1'
import grid2 from '../bk/grid/column2'
import grid3 from '../bk/grid/column3'
import grid4 from '../bk/grid/column4'
import freeLayout from '../bk/free-layout'

import paragraph from '../bk/paragraph'

// Basic
import button from './button'
 
// Form
 
// 数据
 
// 反馈
 
// 导航
 
// 其他
 
// 组件文档地址
import infoLink from './info-link'
 
const vantComponents = Object.seal([
    grid1,
    grid2,
    grid3,
    grid4,
    freeLayout,
    paragraph,
    button
])
 
export default vantComponents
 
export const vantComponentGroupList = Array.from(new Set(vantComponents.map(item => item.group)))
 
export const vanLink = infoLink
