import request from '@/utils/request'

// 查询软件列表
export function listSoftwareItem(query) {
  return request({
    url: '/tool/software/item/list',
    method: 'get',
    params: query
  })
}

// 查询软件详细（含下载配置）
export function getSoftwareItem(softwareId) {
  return request({
    url: '/tool/software/item/' + softwareId,
    method: 'get'
  })
}

// 新增软件
export function addSoftwareItem(data) {
  return request({
    url: '/tool/software/item',
    method: 'post',
    data: data
  })
}

// 修改软件
export function updateSoftwareItem(data) {
  return request({
    url: '/tool/software/item',
    method: 'put',
    data: data
  })
}

// 删除软件
export function delSoftwareItem(softwareIds) {
  return request({
    url: '/tool/software/item/' + softwareIds,
    method: 'delete'
  })
}

// 修改发布状态
export function changeSoftwarePublishStatus(data) {
  return request({
    url: '/tool/software/item/changePublishStatus',
    method: 'put',
    data: data
  })
}
