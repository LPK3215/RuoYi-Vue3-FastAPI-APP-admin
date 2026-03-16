<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="关键词" prop="softwareName">
        <el-input
          v-model="queryParams.softwareName"
          placeholder="名称 / 描述 / 作者 / 标签..."
          clearable
          style="width: 200px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="分类" prop="categoryId">
        <el-select v-model="queryParams.categoryId" placeholder="请选择分类" clearable style="width: 200px">
          <el-option v-for="c in categoryOptions" :key="c.categoryId" :label="c.categoryName" :value="c.categoryId" />
        </el-select>
      </el-form-item>
      <el-form-item label="发布状态" prop="publishStatus">
        <el-select v-model="queryParams.publishStatus" placeholder="请选择发布状态" clearable style="width: 200px">
          <el-option v-for="o in publishStatusOptions" :key="o.value" :label="o.label" :value="o.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="状态" prop="status">
        <el-select v-model="queryParams.status" placeholder="软件状态" clearable style="width: 200px">
          <el-option v-for="dict in sys_normal_disable" :key="dict.value" :label="dict.label" :value="dict.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="开源" prop="openSource">
        <el-select v-model="queryParams.openSource" placeholder="是否开源" clearable style="width: 200px">
          <el-option label="是" value="1" />
          <el-option label="否" value="0" />
        </el-select>
      </el-form-item>
      <el-form-item label="许可证" prop="license">
        <el-input v-model="queryParams.license" placeholder="MIT / Apache-2.0 ..." clearable style="width: 200px" />
      </el-form-item>
      <el-form-item label="标签" prop="tag">
        <el-input v-model="queryParams.tag" placeholder="例如：dev / note / cli" clearable style="width: 200px" />
      </el-form-item>
      <el-form-item label="平台" prop="platform">
        <el-select v-model="queryParams.platform" placeholder="存在下载配置" clearable style="width: 200px">
          <el-option v-for="p in platformOptions" :key="p.value" :label="p.label" :value="p.value" />
        </el-select>
      </el-form-item>
      <el-form-item label="作者" prop="author">
        <el-input v-model="queryParams.author" placeholder="作者/团队关键词" clearable style="width: 200px" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8 software-toolbar">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['tool:software:item:add']">
          新增
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['tool:software:item:edit']"
        >
          修改
        </el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['tool:software:item:remove']"
        >
          删除
        </el-button>
      </el-col>
      <div class="toolbar-right">
        <el-radio-group v-model="viewMode" class="view-toggle">
          <el-radio-button value="table">
            <el-icon><List /></el-icon>
            列表
          </el-radio-button>
          <el-radio-button value="card">
            <el-icon><Grid /></el-icon>
            卡片
          </el-radio-button>
        </el-radio-group>

        <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
      </div>
    </el-row>

    <el-card shadow="never" class="software-list-card">
      <template #header>
        <div class="card-header">
          <div class="title">
            <span>软件列表</span>
            <el-tag type="info" effect="plain" class="count-tag">{{ total }} 条</el-tag>
          </div>
          <div class="actions">
            <el-button v-if="viewMode === 'card'" icon="Refresh" @click="getList">刷新</el-button>
          </div>
        </div>
      </template>

      <el-table
        v-if="viewMode === 'table'"
        v-loading="loading"
        :data="softwareList"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" align="center" />
        <el-table-column label="软件ID" align="center" prop="softwareId" width="90" />
        <el-table-column label="软件名称" align="center" prop="softwareName" min-width="180" show-overflow-tooltip />
        <el-table-column label="分类" align="center" prop="categoryName" min-width="120" show-overflow-tooltip />
        <el-table-column label="开源" align="center" prop="openSource" width="90">
          <template #default="scope">
            <el-tag :type="scope.row.openSource === '1' ? 'success' : 'info'">
              {{ scope.row.openSource === '1' ? '是' : '否' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="许可证" align="center" prop="license" min-width="120" show-overflow-tooltip />
        <el-table-column label="标签" align="center" prop="tags" min-width="140" show-overflow-tooltip />
        <el-table-column label="作者/团队" align="center" min-width="140" show-overflow-tooltip>
          <template #default="scope">
            <span>{{ scope.row.author || scope.row.team || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="发布状态" align="center" prop="publishStatus" width="100">
          <template #default="scope">
            <el-tag :type="publishStatusTagType(scope.row.publishStatus)">
              {{ publishStatusLabel(scope.row.publishStatus) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" align="center" prop="status" width="90">
          <template #default="scope">
            <dict-tag :options="sys_normal_disable" :value="scope.row.status" />
          </template>
        </el-table-column>
        <el-table-column label="排序" align="center" prop="softwareSort" width="90" />
        <el-table-column label="更新时间" align="center" prop="updateTime" width="180">
          <template #default="scope">
            <span>{{ parseTime(scope.row.updateTime) }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="320" align="center" class-name="small-padding fixed-width">
          <template #default="scope">
            <el-button link type="primary" icon="View" @click="goDetail(scope.row)">详情</el-button>
            <el-button
              link
              type="primary"
              icon="Edit"
              @click="handleUpdate(scope.row)"
              v-hasPermi="['tool:software:item:edit']"
            >
              修改
            </el-button>
            <el-button
              link
              type="primary"
              icon="Delete"
              @click="handleDelete(scope.row)"
              v-hasPermi="['tool:software:item:remove']"
            >
              删除
            </el-button>
            <el-button
              link
              type="primary"
              icon="Upload"
              v-hasPermi="['tool:software:item:publish']"
              @click="handlePublish(scope.row)"
            >
              {{ scope.row.publishStatus === '1' ? '下架' : '上架' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-else v-loading="loading" class="card-view">
        <el-empty v-if="!softwareList.length" description="暂无数据" />
        <div v-else class="card-grid">
          <el-card
            v-for="item in softwareList"
            :key="item.softwareId"
            class="software-card"
            shadow="hover"
            role="button"
            tabindex="0"
            @click="goDetail(item)"
            @keydown.enter.prevent="goDetail(item)"
            @keydown.space.prevent="goDetail(item)"
          >
            <template #header>
              <div class="software-card-header">
                <div class="left">
                  <el-avatar class="icon" shape="square" :size="40" :src="item.iconUrl">
                    {{ (item.softwareName || '').slice(0, 1) }}
                  </el-avatar>
                  <div class="heading">
                    <div class="name" :title="item.softwareName">{{ item.softwareName || '-' }}</div>
                    <div class="meta">
                      <el-tag v-if="item.categoryName" size="small" effect="plain">{{ item.categoryName }}</el-tag>
                      <el-tag size="small" :type="item.openSource === '1' ? 'success' : 'info'" effect="plain">
                        {{ item.openSource === '1' ? '开源' : '闭源' }}
                      </el-tag>
                      <el-tag size="small" :type="publishStatusTagType(item.publishStatus)" effect="plain">
                        {{ publishStatusLabel(item.publishStatus) }}
                      </el-tag>
                    </div>
                  </div>
                </div>
                <div class="right">
                  <dict-tag :options="sys_normal_disable" :value="item.status" />
                </div>
              </div>
            </template>

            <div class="software-card-body">
              <div class="desc">
                <span v-if="item.shortDesc">{{ item.shortDesc }}</span>
                <span v-else class="muted">暂无简短描述</span>
              </div>

              <div class="kv">
                <div class="kv-item">
                  <span class="k">许可证</span>
                  <span class="v">{{ item.license || '-' }}</span>
                </div>
                <div class="kv-item">
                  <span class="k">作者/团队</span>
                  <span class="v">{{ item.author || item.team || '-' }}</span>
                </div>
              </div>

              <div v-if="tagList(item).length" class="tag-list">
                <el-tag v-for="t in tagList(item).slice(0, 6)" :key="t" size="small" effect="plain">{{ t }}</el-tag>
                <el-tag v-if="tagList(item).length > 6" size="small" type="info" effect="plain">
                  +{{ tagList(item).length - 6 }}
                </el-tag>
              </div>

              <div class="links" v-if="item.officialUrl || item.repoUrl">
                <el-link
                  v-if="item.officialUrl"
                  :href="item.officialUrl"
                  target="_blank"
                  rel="noopener noreferrer"
                  underline="never"
                  @click.stop
                >
                  官网
                </el-link>
                <el-link
                  v-if="item.repoUrl"
                  :href="item.repoUrl"
                  target="_blank"
                  rel="noopener noreferrer"
                  underline="never"
                  @click.stop
                >
                  仓库
                </el-link>
              </div>
            </div>

            <div class="software-card-actions">
              <el-button link type="primary" icon="View" @click.stop="goDetail(item)">详情</el-button>
              <el-button
                link
                type="primary"
                icon="Edit"
                @click.stop="handleUpdate(item)"
                v-hasPermi="['tool:software:item:edit']"
              >
                编辑
              </el-button>
              <el-button
                link
                type="primary"
                icon="Upload"
                v-hasPermi="['tool:software:item:publish']"
                @click.stop="handlePublish(item)"
              >
                {{ item.publishStatus === '1' ? '下架' : '上架' }}
              </el-button>
              <el-button
                link
                type="danger"
                icon="Delete"
                @click.stop="handleDelete(item)"
                v-hasPermi="['tool:software:item:remove']"
              >
                删除
              </el-button>
            </div>
          </el-card>
        </div>
      </div>

      <pagination
        v-show="total > 0"
        :total="total"
        v-model:page="queryParams.pageNum"
        v-model:limit="queryParams.pageSize"
        @pagination="getList"
      />
    </el-card>

    <!-- 添加或修改软件对话框 -->
    <el-dialog :title="title" v-model="open" width="980px" append-to-body>
      <el-form ref="softwareRef" :model="form" :rules="rules" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="软件名称" prop="softwareName">
              <el-input v-model="form.softwareName" placeholder="请输入软件名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="分类" prop="categoryId">
              <el-select v-model="form.categoryId" placeholder="请选择分类" filterable style="width: 100%">
                <el-option
                  v-for="c in categoryOptions"
                  :key="c.categoryId"
                  :label="c.categoryName"
                  :value="c.categoryId"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="发布状态" prop="publishStatus">
              <el-select v-model="form.publishStatus" placeholder="请选择发布状态" style="width: 100%">
                <el-option v-for="o in publishStatusOptions" :key="o.value" :label="o.label" :value="o.value" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="状态" prop="status">
              <el-radio-group v-model="form.status">
                <el-radio v-for="dict in sys_normal_disable" :key="dict.value" :value="dict.value">
                  {{ dict.label }}
                </el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="排序" prop="softwareSort">
              <el-input-number v-model="form.softwareSort" controls-position="right" :min="0" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="图标" prop="iconUrl">
              <ImageUpload v-model="form.iconUrl" :limit="1" :fileSize="2" :fileType="['png', 'jpg', 'jpeg', 'svg']" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="简短描述" prop="shortDesc">
          <el-input v-model="form.shortDesc" type="textarea" :autosize="{ minRows: 2, maxRows: 4 }" placeholder="可选：一句话描述" />
        </el-form-item>

        <el-divider content-position="left">元信息</el-divider>
        <el-row :gutter="20">
          <el-col :span="6">
            <el-form-item label="开源" prop="openSource">
              <el-switch v-model="form.openSource" active-value="1" inactive-value="0" />
            </el-form-item>
          </el-col>
          <el-col :span="18">
            <el-form-item label="许可证" prop="license">
              <el-input v-model="form.license" placeholder="例如：MIT / Apache-2.0 / GPL-3.0" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item label="标签" prop="tags">
          <el-input v-model="form.tags" placeholder="逗号分隔，例如：dev,cli,tool" />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="官网" prop="officialUrl">
              <el-input v-model="form.officialUrl" placeholder="https://..." />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="仓库" prop="repoUrl">
              <el-input v-model="form.repoUrl" placeholder="https://github.com/..." />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="作者" prop="author">
              <el-input v-model="form.author" placeholder="可选" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="团队" prop="team">
              <el-input v-model="form.team" placeholder="可选" />
            </el-form-item>
          </el-col>
        </el-row>

        <el-tabs v-model="activeMdTab" type="border-card">
          <el-tab-pane label="介绍（Markdown）" name="desc">
            <el-row :gutter="12">
              <el-col :span="12">
                <el-input
                  v-model="form.descriptionMd"
                  type="textarea"
                  :autosize="{ minRows: 14, maxRows: 20 }"
                  placeholder="支持 Markdown，左侧编辑，右侧预览"
                />
              </el-col>
              <el-col :span="12">
                <div class="md-preview">
                  <MarkdownRender :content="form.descriptionMd || ''" />
                </div>
              </el-col>
            </el-row>
          </el-tab-pane>
          <el-tab-pane label="使用说明（Markdown）" name="usage">
            <el-row :gutter="12">
              <el-col :span="12">
                <el-input
                  v-model="form.usageMd"
                  type="textarea"
                  :autosize="{ minRows: 14, maxRows: 20 }"
                  placeholder="支持 Markdown，左侧编辑，右侧预览"
                />
              </el-col>
              <el-col :span="12">
                <div class="md-preview">
                  <MarkdownRender :content="form.usageMd || ''" />
                </div>
              </el-col>
            </el-row>
          </el-tab-pane>
        </el-tabs>

        <el-divider content-position="left">多平台下载配置</el-divider>
        <el-row class="mb8">
          <el-col :span="24">
            <el-button type="primary" plain icon="Plus" @click="handleAddDownloadRow">新增下载</el-button>
          </el-col>
        </el-row>

        <el-table :data="form.downloads" border>
          <el-table-column label="平台" prop="platform" width="140">
            <template #default="scope">
              <el-select v-model="scope.row.platform" placeholder="平台" clearable style="width: 120px">
                <el-option v-for="p in platformOptions" :key="p.value" :label="p.label" :value="p.value" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="下载地址" prop="downloadUrl" min-width="260">
            <template #default="scope">
              <el-input v-model="scope.row.downloadUrl" placeholder="https://..." />
            </template>
          </el-table-column>
          <el-table-column label="版本" prop="version" width="120">
            <template #default="scope">
              <el-input v-model="scope.row.version" placeholder="可选" />
            </template>
          </el-table-column>
          <el-table-column label="校验值" prop="checksum" width="160">
            <template #default="scope">
              <el-input v-model="scope.row.checksum" placeholder="可选" />
            </template>
          </el-table-column>
          <el-table-column label="排序" prop="sort" width="90">
            <template #default="scope">
              <el-input-number v-model="scope.row.sort" controls-position="right" :min="0" style="width: 70px" />
            </template>
          </el-table-column>
          <el-table-column label="备注" prop="remark" width="180">
            <template #default="scope">
              <el-input v-model="scope.row.remark" placeholder="可选" />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="80" align="center">
            <template #default="scope">
              <el-button link type="primary" icon="Delete" @click="handleRemoveDownloadRow(scope.$index)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>

        <el-divider content-position="left">资源（仅 URL）</el-divider>
        <el-row class="mb8">
          <el-col :span="24">
            <el-button type="primary" plain icon="Plus" @click="handleAddResourceRow">新增资源</el-button>
          </el-col>
        </el-row>

        <el-table :data="form.resources" border>
          <el-table-column label="类型" prop="resourceType" width="140">
            <template #default="scope">
              <el-select v-model="scope.row.resourceType" placeholder="类型" clearable style="width: 120px">
                <el-option v-for="t in resourceTypeOptions" :key="t.value" :label="t.label" :value="t.value" />
              </el-select>
            </template>
          </el-table-column>
          <el-table-column label="标题" prop="title" width="180">
            <template #default="scope">
              <el-input v-model="scope.row.title" placeholder="可选" />
            </template>
          </el-table-column>
          <el-table-column label="URL" prop="resourceUrl" min-width="260">
            <template #default="scope">
              <el-input v-model="scope.row.resourceUrl" placeholder="https://..." />
            </template>
          </el-table-column>
          <el-table-column label="排序" prop="sort" width="90">
            <template #default="scope">
              <el-input-number v-model="scope.row.sort" controls-position="right" :min="0" style="width: 70px" />
            </template>
          </el-table-column>
          <el-table-column label="备注" prop="remark" width="180">
            <template #default="scope">
              <el-input v-model="scope.row.remark" placeholder="可选" />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="80" align="center">
            <template #default="scope">
              <el-button link type="primary" icon="Delete" @click="handleRemoveResourceRow(scope.$index)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-form>

      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="SoftwareItem">
import { MarkdownRender } from 'markstream-vue'
import 'markstream-vue/index.css'

import { listSoftwareCategoryOptions } from '@/api/tool/software/category'
import {
  addSoftwareItem,
  changeSoftwarePublishStatus,
  delSoftwareItem,
  getSoftwareItem,
  listSoftwareItem,
  updateSoftwareItem
} from '@/api/tool/software/item'

const { proxy } = getCurrentInstance()
const { sys_normal_disable } = proxy.useDict('sys_normal_disable')

const softwareList = ref([])
const categoryOptions = ref([])
const open = ref(false)
const loading = ref(true)
const showSearch = ref(true)
const ids = ref([])
const single = ref(true)
const multiple = ref(true)
const total = ref(0)
const title = ref('')
const activeMdTab = ref('desc')

const router = useRouter()

const viewModeStorageKey = 'tool:software:item:viewMode'
const viewMode = ref('table')

function loadViewMode() {
  try {
    const cached = localStorage.getItem(viewModeStorageKey)
    viewMode.value = cached === 'card' ? 'card' : 'table'
  } catch (e) {
    viewMode.value = 'table'
  }
}

const publishStatusOptions = [
  { label: '草稿', value: '0' },
  { label: '上架', value: '1' },
  { label: '下架', value: '2' }
]

const platformOptions = [
  { label: 'Windows', value: 'windows' },
  { label: 'macOS', value: 'mac' },
  { label: 'Linux', value: 'linux' },
  { label: 'Android', value: 'android' },
  { label: 'iOS', value: 'ios' },
  { label: 'Web', value: 'web' },
  { label: '其他', value: 'other' }
]

const resourceTypeOptions = [
  { label: '截图', value: 'screenshot' },
  { label: '文档', value: 'doc' },
  { label: '链接', value: 'link' },
  { label: '视频', value: 'video' },
  { label: '其他', value: 'other' }
]

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    softwareName: undefined,
    categoryId: undefined,
    publishStatus: undefined,
    status: undefined,
    openSource: undefined,
    license: undefined,
    tag: undefined,
    platform: undefined,
    author: undefined
  },
  rules: {
    softwareName: [{ required: true, message: '软件名称不能为空', trigger: 'blur' }],
    categoryId: [{ required: true, message: '分类不能为空', trigger: 'change' }],
    softwareSort: [{ required: true, message: '排序不能为空', trigger: 'blur' }]
  }
})

const { queryParams, form, rules } = toRefs(data)

function publishStatusLabel(value) {
  return publishStatusOptions.find((o) => o.value === value)?.label || '-'
}

function publishStatusTagType(value) {
  if (value === '1') return 'success'
  if (value === '2') return 'warning'
  return 'info'
}

function clearSelection() {
  ids.value = []
  single.value = true
  multiple.value = true
}

watch(
  () => viewMode.value,
  (val) => {
    try {
      localStorage.setItem(viewModeStorageKey, val)
    } catch (e) {}
    clearSelection()
  }
)

function goDetail(row) {
  const softwareId = row?.softwareId
  if (!softwareId) return
  router.push({ path: '/software/detail', query: { softwareId } })
}

function tagList(row) {
  const raw = row?.tags
  if (!raw) return []
  return String(raw)
    .split(',')
    .map((s) => s.trim())
    .filter(Boolean)
}

function getCategoryOptions() {
  listSoftwareCategoryOptions().then((res) => {
    categoryOptions.value = res.data || []
  })
}

function getList() {
  loading.value = true
  listSoftwareItem(queryParams.value).then((response) => {
    softwareList.value = response.rows || []
    total.value = response.total || 0
    loading.value = false
  })
}

function cancel() {
  open.value = false
  reset()
}

function reset() {
  form.value = {
    softwareId: undefined,
    categoryId: undefined,
    softwareName: undefined,
    shortDesc: undefined,
    iconUrl: undefined,
    officialUrl: undefined,
    repoUrl: undefined,
    author: undefined,
    team: undefined,
    license: undefined,
    openSource: '0',
    tags: undefined,
    descriptionMd: undefined,
    usageMd: undefined,
    publishStatus: '0',
    softwareSort: 0,
    status: '0',
    downloads: [],
    resources: []
  }
  activeMdTab.value = 'desc'
  proxy.resetForm('softwareRef')
}

function handleQuery() {
  queryParams.value.pageNum = 1
  getList()
}

function resetQuery() {
  proxy.resetForm('queryRef')
  handleQuery()
}

function handleSelectionChange(selection) {
  ids.value = selection.map((item) => item.softwareId)
  single.value = selection.length !== 1
  multiple.value = !selection.length
}

function handleAdd() {
  reset()
  open.value = true
  title.value = '新增软件'
}

function handleUpdate(row) {
  reset()
  const softwareId = row?.softwareId || ids.value[0]
  getSoftwareItem(softwareId).then((response) => {
    form.value = {
      ...form.value,
      ...response.data,
      downloads: response.data?.downloads || [],
      resources: response.data?.resources || []
    }
    open.value = true
    title.value = '修改软件'
  })
}

function handleDelete(row) {
  const softwareIds = row?.softwareId || ids.value.join(',')
  proxy.$modal
    .confirm('是否确认删除软件编号为 "' + softwareIds + '" 的数据项？')
    .then(() => delSoftwareItem(softwareIds))
    .then(() => {
      getList()
      proxy.$modal.msgSuccess('删除成功')
    })
    .catch(() => {})
}

function validateDownloads() {
  if (!form.value.downloads || !form.value.downloads.length) return true
  for (const [index, d] of form.value.downloads.entries()) {
    if (!d.platform || !d.downloadUrl) {
      proxy.$modal.msgError(`第 ${index + 1} 行下载配置未填写完整（平台/下载地址必填）`)
      return false
    }
  }
  return true
}

function validateResources() {
  if (!form.value.resources || !form.value.resources.length) return true
  for (const [index, r] of form.value.resources.entries()) {
    if (!r.resourceType || !r.resourceUrl) {
      proxy.$modal.msgError(`第 ${index + 1} 行资源未填写完整（类型/URL必填）`)
      return false
    }
  }
  return true
}

function submitForm() {
  proxy.$refs['softwareRef'].validate((valid) => {
    if (!valid) return
    if (!validateDownloads()) return
    if (!validateResources()) return
    const request = form.value.softwareId ? updateSoftwareItem : addSoftwareItem
    request(form.value).then(() => {
      proxy.$modal.msgSuccess('操作成功')
      open.value = false
      getList()
    })
  })
}

function handleAddDownloadRow() {
  if (!form.value.downloads) form.value.downloads = []
  form.value.downloads.push({
    platform: undefined,
    downloadUrl: undefined,
    version: undefined,
    checksum: undefined,
    sort: 0,
    remark: undefined
  })
}

function handleRemoveDownloadRow(index) {
  form.value.downloads.splice(index, 1)
}

function handleAddResourceRow() {
  if (!form.value.resources) form.value.resources = []
  form.value.resources.push({
    resourceType: undefined,
    title: undefined,
    resourceUrl: undefined,
    sort: 0,
    remark: undefined
  })
}

function handleRemoveResourceRow(index) {
  form.value.resources.splice(index, 1)
}

function handlePublish(row) {
  const next = row.publishStatus === '1' ? '2' : '1'
  const text = next === '1' ? '上架' : '下架'
  proxy.$modal
    .confirm(`确认要${text}【${row.softwareName}】吗？`)
    .then(() => changeSoftwarePublishStatus({ softwareId: row.softwareId, publishStatus: next }))
    .then(() => {
      proxy.$modal.msgSuccess('操作成功')
      getList()
    })
    .catch(() => {})
}

getCategoryOptions()
loadViewMode()
getList()
</script>

<style scoped>
.software-toolbar {
  align-items: center;
}

.toolbar-right {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 10px;
}

.toolbar-right :deep(.top-right-btn) {
  margin-left: 0;
}

.view-toggle :deep(.el-radio-button__inner) {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.software-list-card :deep(.el-card__body) {
  padding-top: 8px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.card-header .title {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
}

.actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.card-view {
  min-height: 240px;
}

.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 12px;
}

.software-card {
  cursor: pointer;
  transition: box-shadow 200ms ease, transform 200ms ease;
}

.software-card:hover {
  transform: translateY(-2px);
}

.software-card:focus {
  outline: 2px solid var(--el-color-primary);
  outline-offset: 2px;
}

@media (prefers-reduced-motion: reduce) {
  .software-card {
    transition: none;
  }
  .software-card:hover {
    transform: none;
  }
}

.software-card-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.software-card-header .left {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.software-card-header .heading {
  min-width: 0;
}

.software-card-header .name {
  font-weight: 600;
  line-height: 20px;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.software-card-header .meta {
  margin-top: 6px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.software-card-body {
  padding: 2px 2px 0;
}

.desc {
  color: var(--el-text-color-regular);
  line-height: 20px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 40px;
}

.muted {
  color: var(--el-text-color-secondary);
}

.kv {
  margin-top: 10px;
  display: grid;
  grid-template-columns: 1fr;
  gap: 8px;
}

.kv-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
}

.kv-item .k {
  color: var(--el-text-color-secondary);
  white-space: nowrap;
}

.kv-item .v {
  color: var(--el-text-color-regular);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 220px;
}

.tag-list {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.links {
  margin-top: 10px;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.software-card-actions {
  margin-top: 12px;
  padding-top: 10px;
  border-top: 1px solid var(--el-border-color-lighter);
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.md-preview {
  border: 1px solid var(--el-border-color);
  border-radius: 4px;
  padding: 10px 12px;
  min-height: 320px;
  max-height: 520px;
  overflow: auto;
}
</style>
