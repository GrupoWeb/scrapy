<template>
  <div class="container">
    <el-card shadow="always">
      <div slot="header">
        <span>Catálogo de categorias</span>
      </div>
      <el-form :model="API.form" ref="form"  label-width="80px" :inline="false" >
        <el-form-item label="Nombre.">
          <el-input v-model="API.form.name"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="setCategories">Guardar</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <div class="mt-3">
      <el-card shadow="always">
        <el-table :data="API.res.categories" border stripe empty-text="Sin datos">
          <el-table-column label="Código" prop="code"></el-table-column>
          <el-table-column label="Nombre" prop="name"></el-table-column>
          <el-table-column label="Opciones">
            <template slot-scope="scope">
               <el-button type="danger" icon="el-icon-delete" circle @click="deleteCategorie(scope.row.code)"></el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </div>
    
  </div>
</template>

<script>
import axios from 'axios'
  export default {
    data(){
      return {
        path: 'http://localhost:5000/',
        API: {
          form :{
            name: ""
          },
          router: {
            categories: 'http://localhost:5000/categorie',
            getcategories: 'http://localhost:5000/categories',
            categoriesD: 'http://localhost:5000/categoriesD',
          },
          res: {
            categories:[]
          },
        }
      }
    },
    mounted() {
      this.getCategories();
    },
    methods: {
      setCategories(){
        axios.post(this.API.router.categories,{
          name: this.API.form.name
        })
        .then(response => {
            this.$swal({
              position: "top-end",
              icon: "success",
              title: "Dato ingresado",
              showConfirmButton: false,
              timer: 2500,
            });
            this.API.form.name = ""
            this.getCategories();
        })
      },
      getCategories() {
        axios.get(this.API.router.getcategories)
        .then(response => {
          this.API.res.categories = response.data
          console.log(response.data)
        } )
      },
      deleteCategorie(id) {
        axios.post(this.API.router.categoriesD,{id: id})
        .then(response => {
          if(response.data == 'ok'){
            this.$swal({
              position: "top-end",
              icon: "success",
              title: "Se elimino correctamente",
              showConfirmButton: false,
              timer: 2500,
            });
            this.getCategories();
          }
        })
      }
    }
  }
</script>
