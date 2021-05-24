<template>
  <div class="container">
    <el-card shadow="always">
      <div slot="header">
        <span>Catálogo de Búsqueda</span>
      </div>
      <el-form :model="API.form" ref="form"  label-width="120px" :inline="false" >
        <el-form-item label="Nombre:">
          <el-input v-model="API.form.name"></el-input>
        </el-form-item>
        <el-form-item label="Catálogo:">

          <el-select v-model="API.form.categorie"  clearable filterable placeholder="Categorias" class="selectall">
            <el-option v-for="item in API.res.listCategories"
              :key="item.code"
              :label="item.name"
              :value="item.code">
            </el-option>
          </el-select>
          
        </el-form-item>
        <el-form-item label="Productos:">

          <el-select v-model="API.form.product" multiple clearable filterable placeholder="Productos" class="selectall">
            <el-option v-for="item in API.res.listProducts"
              :key="item.code"
              :label="item.name"
              :value="item.code">
            </el-option>
          </el-select>

        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="setSearchMaster">Guardar</el-button>
        </el-form-item>
      </el-form>
    </el-card>
    <div class="mt-3">
      <el-card shadow="always">
        <el-table :data="API.res.listMaster " border stripe empty-text="Sin datos">
          <el-table-column label="Código" prop="code"></el-table-column>
          <el-table-column label="Nombre" prop="name"></el-table-column>
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
            name: "",
            categorie: "",
            product: [],
          },
          router: {
            getCategories: 'http://localhost:5000/categories',
            getProducts: 'http://localhost:5000/products',
            getSearch: 'http://localhost:5000/productD',
            setSearch: 'http://localhost:5000/search',
            search: 'http://localhost:5000/search',
          },
          res: {
            categories:[],
            listCategories:[],
            listProducts:[],
            listMaster:[]
          },
        }
      }
    },
    mounted() {
      this.getCategories();
      this.getProducts();
      this.getSearchMaster();
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
        axios.get(this.API.router.getCategories)
        .then(response => {
          this.API.res.listCategories = response.data
        } )
      },
      getProducts() {
        axios.get(this.API.router.getProducts)
        .then(response => {
          this.API.res.listProducts = response.data
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
      },

      setSearchMaster(){
        axios.post(this.API.router.setSearch,{
          name: this.API.form.name,
          categorie: this.API.form.categorie,
          products: this.API.form.product
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
            this.API.form.categorie = ""
            this.API.form.product = []
            this.getSearchMaster();
        })
      },
      getSearchMaster(){
        axios.get(this.API.router.search)
          .then(response => {
            this.API.res.listMaster = response.data
          })
      }
    }
  }
</script>

<style>
.selectall{
  width: 100%;
}
</style>
