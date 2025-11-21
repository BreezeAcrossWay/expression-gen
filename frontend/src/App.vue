<template>
  <div id="app">
    <div class="container">
      <header class="header">
        <h1>🎭 明星表情包生成器</h1>
        <p class="subtitle">上传明星照片，一键生成专属卡通表情包</p>
      </header>

      <!-- 步骤指示器 -->
      <el-steps :active="currentStep" align-center class="steps">
        <el-step title="上传照片" description="选择明星照片" />
        <el-step title="选择形象" description="挑选卡通风格" />
        <el-step title="生成表情" description="制作表情包" />
        <el-step title="导出下载" description="保存表情包" />
      </el-steps>

      <!-- 步骤1: 上传照片 -->
      <div v-if="currentStep === 0" class="step-content">
        <el-upload
          class="upload-demo"
          drag
          :action="uploadUrl"
          :on-success="handleUploadSuccess"
          :on-error="handleUploadError"
          :before-upload="beforeUpload"
          :show-file-list="false"
          accept="image/*"
        >
          <el-icon class="el-icon--upload"><upload-filled /></el-icon>
          <div class="el-upload__text">
            将照片拖到此处，或<em>点击上传</em>
          </div>
          <template #tip>
            <div class="el-upload__tip">
              支持 jpg/png/gif 格式，文件大小不超过 16MB
            </div>
          </template>
        </el-upload>
      </div>

      <!-- 步骤2: 选择卡通形象 -->
      <div v-if="currentStep === 1" class="step-content">
        <h2 class="section-title">选择你最喜欢的卡通形象</h2>
        <div class="variants-grid">
          <div
            v-for="variant in variants"
            :key="variant.id"
            class="variant-card"
            :class="{ selected: selectedVariant?.id === variant.id }"
            @click="selectVariant(variant)"
          >
            <img :src="variant.url" :alt="variant.style" />
            <div class="variant-label">{{ variant.style }}</div>
            <div v-if="selectedVariant?.id === variant.id" class="selected-badge">
              <el-icon><check /></el-icon>
            </div>
          </div>
        </div>
        <div class="button-group">
          <el-button @click="currentStep = 0">上一步</el-button>
          <el-button type="primary" @click="generateDefaultExpressions" :disabled="!selectedVariant">
            生成表情包
          </el-button>
        </div>
      </div>

      <!-- 步骤3: 生成和管理表情包 -->
      <div v-if="currentStep === 2" class="step-content">
        <div class="expressions-header">
          <h2 class="section-title">表情包管理</h2>
          <div class="custom-input-group">
            <el-input
              v-model="customPrompt"
              placeholder="输入自定义提示词，如：生气、大笑、委屈..."
              class="custom-prompt-input"
            />
            <el-button type="primary" @click="generateCustomExpression" :loading="generating">
              生成自定义表情
            </el-button>
          </div>
        </div>

        <div class="expressions-grid">
          <div
            v-for="expr in expressions"
            :key="expr.id"
            class="expression-card"
          >
            <img :src="expr.url" :alt="expr.expression" />
            <div class="expression-footer">
              <span class="expression-label">
                {{ expr.custom_prompt || expr.expression }}
              </span>
              <div class="expression-actions">
                <el-button
                  size="small"
                  type="primary"
                  @click="exportSingle(expr.id)"
                >
                  <el-icon><download /></el-icon>
                </el-button>
                <el-button
                  size="small"
                  type="danger"
                  @click="deleteExpression(expr.id)"
                >
                  <el-icon><delete /></el-icon>
                </el-button>
              </div>
            </div>
          </div>
        </div>

        <div class="button-group">
          <el-button @click="currentStep = 1">上一步</el-button>
          <el-button type="success" @click="exportAll" :disabled="expressions.length === 0">
            <el-icon><download /></el-icon>
            一键导出全部 ({{ expressions.length }}个)
          </el-button>
          <el-button type="primary" @click="currentStep = 3">
            完成
          </el-button>
        </div>
      </div>

      <!-- 步骤4: 完成 -->
      <div v-if="currentStep === 3" class="step-content completion">
        <div class="success-icon">
          <el-icon><circle-check /></el-icon>
        </div>
        <h2>🎉 表情包制作完成！</h2>
        <p>你已成功创建 {{ expressions.length }} 个表情包</p>
        <div class="button-group">
          <el-button type="primary" @click="reset">
            制作新的表情包
          </el-button>
          <el-button type="success" @click="exportAll" v-if="expressions.length > 0">
            再次导出全部
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'
import axios from 'axios'
import {
  UploadFilled,
  Check,
  Download,
  Delete,
  CircleCheck
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'App',
  components: {
    UploadFilled,
    Check,
    Download,
    Delete,
    CircleCheck
  },
  setup() {
    const currentStep = ref(0)
    const variants = ref([])
    const selectedVariant = ref(null)
    const expressions = ref([])
    const customPrompt = ref('')
    const generating = ref(false)
    const uploadUrl = ref('/api/upload')

    const beforeUpload = (file) => {
      const isImage = file.type.startsWith('image/')
      const isLt16M = file.size / 1024 / 1024 < 16

      if (!isImage) {
        ElMessage.error('只能上传图片文件!')
        return false
      }
      if (!isLt16M) {
        ElMessage.error('图片大小不能超过 16MB!')
        return false
      }
      return true
    }

    const handleUploadSuccess = (response) => {
      if (response.success) {
        variants.value = response.variants
        currentStep.value = 1
        ElMessage.success('上传成功！请选择喜欢的卡通形象')
      } else {
        ElMessage.error(response.error || '上传失败')
      }
    }

    const handleUploadError = () => {
      ElMessage.error('上传失败，请重试')
    }

    const selectVariant = (variant) => {
      selectedVariant.value = variant
    }

    const generateDefaultExpressions = async () => {
      if (!selectedVariant.value) {
        ElMessage.warning('请先选择一个卡通形象')
        return
      }

      generating.value = true
      try {
        const response = await axios.post('/api/generate-expressions', {
          variant_id: selectedVariant.value.id,
          expressions: ['开心', '难过', '思考']
        })

        if (response.data.success) {
          expressions.value = response.data.expressions
          currentStep.value = 2
          ElMessage.success('表情包生成成功！')
        }
      } catch (error) {
        ElMessage.error('生成失败：' + error.message)
      } finally {
        generating.value = false
      }
    }

    const generateCustomExpression = async () => {
      if (!customPrompt.value.trim()) {
        ElMessage.warning('请输入自定义提示词')
        return
      }

      generating.value = true
      try {
        const response = await axios.post('/api/generate-custom', {
          variant_id: selectedVariant.value.id,
          prompt: customPrompt.value
        })

        if (response.data.success) {
          expressions.value.push(response.data.expression)
          customPrompt.value = ''
          ElMessage.success('自定义表情生成成功！')
        }
      } catch (error) {
        ElMessage.error('生成失败：' + error.message)
      } finally {
        generating.value = false
      }
    }

    const deleteExpression = async (expressionId) => {
      try {
        await axios.delete(`/api/delete-expression/${expressionId}`)
        expressions.value = expressions.value.filter(e => e.id !== expressionId)
        ElMessage.success('删除成功')
      } catch (error) {
        ElMessage.error('删除失败：' + error.message)
      }
    }

    const exportSingle = (expressionId) => {
      window.open(`/api/export-single/${expressionId}`, '_blank')
      ElMessage.success('开始下载')
    }

    const exportAll = async () => {
      if (expressions.value.length === 0) {
        ElMessage.warning('没有可导出的表情包')
        return
      }

      try {
        const expressionIds = expressions.value.map(e => e.id)
        const response = await axios.post('/api/export-all', {
          expression_ids: expressionIds
        }, {
          responseType: 'blob'
        })

        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'all_expressions.zip')
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)

        ElMessage.success('全部表情包已导出！')
      } catch (error) {
        ElMessage.error('导出失败：' + error.message)
      }
    }

    const reset = () => {
      currentStep.value = 0
      variants.value = []
      selectedVariant.value = null
      expressions.value = []
      customPrompt.value = ''
    }

    return {
      currentStep,
      variants,
      selectedVariant,
      expressions,
      customPrompt,
      generating,
      uploadUrl,
      beforeUpload,
      handleUploadSuccess,
      handleUploadError,
      selectVariant,
      generateDefaultExpressions,
      generateCustomExpression,
      deleteExpression,
      exportSingle,
      exportAll,
      reset
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
  padding: 20px;
}

#app {
  max-width: 1200px;
  margin: 0 auto;
}

.container {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  font-size: 2.5em;
  color: #333;
  margin-bottom: 10px;
}

.subtitle {
  color: #666;
  font-size: 1.1em;
}

.steps {
  margin-bottom: 50px;
}

.step-content {
  min-height: 400px;
}

.section-title {
  text-align: center;
  font-size: 1.8em;
  color: #333;
  margin-bottom: 30px;
}

/* 上传区域 */
.upload-demo {
  max-width: 600px;
  margin: 0 auto;
}

.el-upload-dragger {
  width: 600px;
  height: 300px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.el-icon--upload {
  font-size: 67px;
  color: #409eff;
  margin-bottom: 16px;
}

/* 卡通形象网格 */
.variants-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.variant-card {
  position: relative;
  border: 3px solid #e0e0e0;
  border-radius: 15px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
}

.variant-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.variant-card.selected {
  border-color: #409eff;
  background: #f0f8ff;
}

.variant-card img {
  width: 100%;
  height: 250px;
  object-fit: cover;
  border-radius: 10px;
  margin-bottom: 15px;
}

.variant-label {
  text-align: center;
  font-weight: bold;
  color: #333;
  font-size: 1.1em;
}

.selected-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  width: 40px;
  height: 40px;
  background: #409eff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
}

/* 表情包区域 */
.expressions-header {
  margin-bottom: 30px;
}

.custom-input-group {
  display: flex;
  gap: 15px;
  max-width: 800px;
  margin: 20px auto;
}

.custom-prompt-input {
  flex: 1;
}

.expressions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 25px;
  margin-bottom: 40px;
}

.expression-card {
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  background: white;
  transition: all 0.3s ease;
}

.expression-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.expression-card img {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.expression-footer {
  padding: 15px;
  background: #f8f9fa;
}

.expression-label {
  display: block;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
  text-align: center;
}

.expression-actions {
  display: flex;
  gap: 10px;
  justify-content: center;
}

/* 按钮组 */
.button-group {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

/* 完成页面 */
.completion {
  text-align: center;
  padding: 60px 20px;
}

.success-icon {
  font-size: 100px;
  color: #67c23a;
  margin-bottom: 30px;
}

.completion h2 {
  font-size: 2.5em;
  color: #333;
  margin-bottom: 20px;
}

.completion p {
  font-size: 1.3em;
  color: #666;
  margin-bottom: 40px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .container {
    padding: 20px;
  }

  .header h1 {
    font-size: 1.8em;
  }

  .variants-grid {
    grid-template-columns: 1fr;
  }

  .expressions-grid {
    grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  }

  .custom-input-group {
    flex-direction: column;
  }

  .button-group {
    flex-direction: column;
  }
}
</style>
