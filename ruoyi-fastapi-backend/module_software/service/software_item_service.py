from datetime import datetime
from typing import Any

from collections import Counter

from sqlalchemy.ext.asyncio import AsyncSession

from common.vo import CrudResponseModel, PageModel
from exceptions.exception import ServiceException
from module_software.dao.software_facets_dao import SoftwareFacetsDao
from module_software.dao.software_category_dao import ToolSoftwareCategoryDao
from module_software.dao.software_item_dao import ToolSoftwareDao, ToolSoftwareDownloadDao, ToolSoftwareResourceDao
from module_software.entity.vo.software_item_vo import (
    DeleteToolSoftwareModel,
    ToolSoftwareDownloadModel,
    ToolSoftwareModel,
    ToolSoftwarePageQueryModel,
    ToolSoftwarePublishStatusModel,
    ToolSoftwareResourceModel,
)
from module_software.entity.vo.software_facets_vo import SoftwareFacetItemModel, SoftwareFacetsModel
from utils.common_util import CamelCaseUtil


class ToolSoftwareService:
    """
    软件信息模块服务层
    """

    @staticmethod
    def _split_tags(tags: str) -> list[str]:
        # 支持中文逗号输入
        raw = (tags or '').replace('，', ',')
        parts = [p.strip() for p in raw.split(',')]
        # 同一软件内的 tag 去重，避免重复计数
        seen: set[str] = set()
        result: list[str] = []
        for p in parts:
            if not p or p in seen:
                continue
            seen.add(p)
            result.append(p)
        return result

    @classmethod
    async def get_facets_services(cls, query_db: AsyncSession, limit: int = 50) -> SoftwareFacetsModel:
        """
        获取后台“软件筛选项”聚合数据（用于构建筛选 UI/下拉选项）。

        仅排除软删数据。
        """
        safe_limit = max(1, min(int(limit or 50), 200))

        # tags: 逗号分隔字段，使用 Python 统计
        tag_strings = await SoftwareFacetsDao.get_tag_strings(query_db, mode='tool')
        tag_counter: Counter[str] = Counter()
        for s in tag_strings:
            for tag in cls._split_tags(s):
                tag_counter[tag] += 1
        tag_items = [
            SoftwareFacetItemModel(value=v, count=c)
            for v, c in sorted(tag_counter.items(), key=lambda x: (-x[1], x[0]))[:safe_limit]
        ]

        license_rows = await SoftwareFacetsDao.get_group_counts(query_db, mode='tool', field_name='license', limit=safe_limit)
        author_rows = await SoftwareFacetsDao.get_group_counts(query_db, mode='tool', field_name='author', limit=safe_limit)
        team_rows = await SoftwareFacetsDao.get_group_counts(query_db, mode='tool', field_name='team', limit=safe_limit)
        platform_rows = await SoftwareFacetsDao.get_platform_counts(query_db, mode='tool', limit=safe_limit)

        return SoftwareFacetsModel(
            tags=tag_items,
            licenses=[SoftwareFacetItemModel(**r) for r in license_rows],
            authors=[SoftwareFacetItemModel(**r) for r in author_rows],
            teams=[SoftwareFacetItemModel(**r) for r in team_rows],
            platforms=[SoftwareFacetItemModel(**r) for r in platform_rows],
        )

    @classmethod
    async def get_software_list_services(
        cls, query_db: AsyncSession, query_object: ToolSoftwarePageQueryModel, is_page: bool = False
    ) -> PageModel[ToolSoftwareModel] | list[dict[str, Any]]:
        """
        获取软件分页列表信息service
        """
        query_result = await ToolSoftwareDao.get_software_list(query_db, query_object, is_page)
        if is_page:
            software_list_result = PageModel[ToolSoftwareModel](
                **{
                    **query_result.model_dump(by_alias=True),
                    'rows': [
                        {
                            **(row[0] or {}),
                            'categoryName': (row[1] or {}).get('categoryName') if isinstance(row[1], dict) else None,
                        }
                        for row in query_result.rows
                    ],
                }
            )
            return software_list_result
        if not query_result:
            return []
        return [
            {**(row[0] or {}), 'categoryName': (row[1] or {}).get('categoryName') if isinstance(row[1], dict) else None}
            for row in query_result
        ]

    @classmethod
    async def software_detail_services(cls, query_db: AsyncSession, software_id: int) -> ToolSoftwareModel:
        """
        获取软件详细信息service（含下载配置/资源URL）
        """
        software = await ToolSoftwareDao.get_software_detail_by_id(query_db, software_id)
        if not software:
            return ToolSoftwareModel()
        software_dict = CamelCaseUtil.transform_result(software)
        category_name = None
        if software.category_id:
            category = await ToolSoftwareCategoryDao.get_category_detail_by_id(query_db, software.category_id)
            if category and category.del_flag == '0':
                category_name = category.category_name
        downloads_do = await ToolSoftwareDownloadDao.get_download_list_by_software_id(query_db, software_id)
        downloads: list[ToolSoftwareDownloadModel] = [
            ToolSoftwareDownloadModel(**CamelCaseUtil.transform_result(item)) for item in downloads_do
        ]

        resources_do = await ToolSoftwareResourceDao.get_resource_list_by_software_id(query_db, software_id)
        resources: list[ToolSoftwareResourceModel] = [
            ToolSoftwareResourceModel(**CamelCaseUtil.transform_result(item)) for item in resources_do
        ]

        return ToolSoftwareModel(
            **{
                **software_dict,
                'categoryName': category_name,
                'downloads': downloads,
                'resources': resources,
            }
        )

    @classmethod
    async def add_software_services(cls, query_db: AsyncSession, page_object: ToolSoftwareModel) -> CrudResponseModel:
        """
        新增软件信息service
        """
        if page_object.category_id is None:
            raise ServiceException(message='分类不能为空')
        category = await ToolSoftwareCategoryDao.get_category_detail_by_id(query_db, page_object.category_id)
        if not category or category.del_flag != '0':
            raise ServiceException(message='分类不存在')
        try:
            db_software = await ToolSoftwareDao.add_software_dao(query_db, page_object)
            await ToolSoftwareDownloadDao.add_downloads_dao(
                query_db, db_software.software_id, page_object.downloads or []
            )
            await ToolSoftwareResourceDao.add_resources_dao(
                query_db, db_software.software_id, page_object.resources or []
            )
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='新增成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def edit_software_services(cls, query_db: AsyncSession, page_object: ToolSoftwareModel) -> CrudResponseModel:
        """
        编辑软件信息service（下载配置/资源URL支持全量覆盖）
        """
        if page_object.software_id is None:
            raise ServiceException(message='软件ID不能为空')
        current = await ToolSoftwareDao.get_software_detail_by_id(query_db, page_object.software_id)
        if not current:
            raise ServiceException(message='软件不存在')
        if page_object.category_id is None:
            raise ServiceException(message='分类不能为空')
        category = await ToolSoftwareCategoryDao.get_category_detail_by_id(query_db, page_object.category_id)
        if not category or category.del_flag != '0':
            raise ServiceException(message='分类不存在')
        fields_set = getattr(page_object, 'model_fields_set', set())
        replace_downloads = 'downloads' in fields_set
        replace_resources = 'resources' in fields_set
        edit_software = page_object.model_dump(exclude_unset=True, exclude={'downloads', 'resources', 'category_name'})
        try:
            await ToolSoftwareDao.edit_software_dao(query_db, edit_software)
            if replace_downloads:
                await ToolSoftwareDownloadDao.delete_downloads_by_software_id(query_db, page_object.software_id)
                await ToolSoftwareDownloadDao.add_downloads_dao(
                    query_db, page_object.software_id, page_object.downloads or []
                )
            if replace_resources:
                await ToolSoftwareResourceDao.delete_resources_by_software_id(query_db, page_object.software_id)
                await ToolSoftwareResourceDao.add_resources_dao(
                    query_db, page_object.software_id, page_object.resources or []
                )
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='更新成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def delete_software_services(
        cls, query_db: AsyncSession, page_object: DeleteToolSoftwareModel, update_by: str
    ) -> CrudResponseModel:
        """
        删除软件信息service（软删）
        """
        if not page_object.software_ids:
            raise ServiceException(message='传入软件id为空')
        software_id_list = page_object.software_ids.split(',')
        try:
            for software_id_str in software_id_list:
                software_id = int(software_id_str)
                current = await ToolSoftwareDao.get_software_detail_by_id(query_db, software_id)
                if not current:
                    raise ServiceException(message='软件不存在')
                await ToolSoftwareDao.delete_software_dao(query_db, software_id, update_by, datetime.now())
                await ToolSoftwareDownloadDao.delete_downloads_by_software_id(query_db, software_id)
                await ToolSoftwareResourceDao.delete_resources_by_software_id(query_db, software_id)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='删除成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc

    @classmethod
    async def change_publish_status_services(
        cls, query_db: AsyncSession, page_object: ToolSoftwarePublishStatusModel, update_by: str
    ) -> CrudResponseModel:
        """
        修改软件发布状态service
        """
        current = await ToolSoftwareDao.get_software_detail_by_id(query_db, page_object.software_id)
        if not current:
            raise ServiceException(message='软件不存在')
        edit_software = ToolSoftwareModel(
            softwareId=page_object.software_id,
            publishStatus=page_object.publish_status,
            updateBy=update_by,
            updateTime=datetime.now(),
        ).model_dump(exclude_unset=True, exclude={'downloads', 'resources', 'category_name'})
        try:
            await ToolSoftwareDao.edit_software_dao(query_db, edit_software)
            await query_db.commit()
            return CrudResponseModel(is_success=True, message='更新成功')
        except Exception as exc:
            await query_db.rollback()
            raise exc
