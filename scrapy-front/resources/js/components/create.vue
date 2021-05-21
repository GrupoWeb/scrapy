<template>
  <div class="col-md-10">
    <el-card shadow="always">
      <div slot="header">
        <span>Listados de Búsqueda personalizadas</span>
      </div>
        <el-form :model="API.form" ref="form" :rules="rules" label-width="80px" :inline="false" >
          <el-form-item label="Categoria:">
            <el-input v-model="API.form.category"></el-input>
          </el-form-item>
          <el-form-item label="Productos:">
            <el-input v-model="API.form.product"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">Guardar</el-button>
            <el-button>Cancelar</el-button>
          </el-form-item>
        </el-form>
        
    </el-card>
    
  </div>
</template>

<script>
  export default {
    data(){
      return {
        API: {
          form: {
            category: "",
            product: ""
          }
        }
      }
    }
  }
</script>
