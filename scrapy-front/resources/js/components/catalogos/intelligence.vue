<template>
    <div class="container">
        <el-card shadow="always">
        <div slot="header">
            <span>Inteligencia de Negocios</span>
        </div>
        <el-form :model="API.form" ref="form"  label-width="120px" :inline="false" >
            <el-form-item label="Nombre:">
                <el-select v-model="API.form.list" clearable filterable class="selectall" placeholder="Busqueda">
                    <el-option v-for="item in API.resp.name_master"
                        :key="item.code"
                        :label="item.name"
                        :value="item.code">
                    </el-option>
                </el-select>
                
            </el-form-item>
            <el-form-item>
            <el-button type="primary" @click="setSearchMaster">Obneter</el-button>
            </el-form-item>
        </el-form>
        </el-card>
        <div v-show="API.Spinner.show">
            <RotateSquare2></RotateSquare2>
        </div>
        <el-row :gutter="20">
            <el-col :span="12" :offset="0">
                <el-card shadow="always" class="mt-5" v-show="API.table.show">
                    <div slot="header">
                        <span>Resultados:</span>
                    </div>
                    <el-table :data="API.resp.table_reponse" border stripe>
                        <el-table-column label="Nombre:" prop="name"></el-table-column>
                        <el-table-column label="Cantidad:" prop="count"></el-table-column>
                    </el-table>
                </el-card>
            </el-col>
            <el-col :span="12" :offset="0">
                <div v-show="API.table.grafic_show" ref="contenedor">
                    <canvas ref="grafica"></canvas>
                </div>
            
            </el-col>
        </el-row>
        
    </div>
</template>

<style>
    .spinner {
    width: 80px!important;
    height: 80px!important;
    margin: 200px auto;
    }

    .spinner:after{
        background: #2596be  !important;
    }
</style>

<script>
import axios from 'axios';
import { RotateSquare2,RotateSquare5 } from "vue-loading-spinner";
import Chart from "chart.js";


    export default {
        components: {
            RotateSquare2,
            RotateSquare5,
             
        },
        data(){
            return {
                API: {
                    form: {
                        list: ""
                    },
                    router: {
                        getIntelligence: "http://localhost:5000/getIntelligence",
                        scrapyn: "http://localhost:5000/scrapyn"
                    },
                    resp: {
                        name_master:[],
                        table_reponse:[]
                    },
                    Spinner: {
                        show: false
                    },
                    table: {
                        show: false,
                        grafic_show: false
                    }
                }
            }
        },
        mounted() {
            this.getIntelligences();
        },
        methods: {
            setSearchMaster() {
                this.API.Spinner.show = true
                this.API.table.show = false
                this.API.table.grafic_show = false
                axios.post(this.API.router.scrapyn,{master_id: this.API.form.list})
                    .then(response => {
                        console.log(response.data)
                        this.API.resp.table_reponse = response.data
                        this.API.Spinner.show = false
                        this.API.table.show = true
                        this.chartDataShow("bar", response.data);
                        this.API.table.grafic_show = true
                        
                    })
            },
            getIntelligences(){
                axios.get(this.API.router.getIntelligence)
                    .then(response => {
                        console.log(response.data)
                        this.API.resp.name_master = response.data
                    })
            },
            chartDataShow(tipe, request) {
            // const remove = this.$refs.grafica.remove();
            const ctx = this.$refs.grafica;
            const legends = this.$refs.leyends;
            //  console.log(request);
            ctx.height = "500";
            ctx.width = "800";
            var dynamicColors = function() {
                var r = Math.floor(Math.random() * 255);
                var g = Math.floor(Math.random() * 255);
                var b = Math.floor(Math.random() * 255);
                return "rgb(" + r + "," + g + "," + b + ")";
            };
            const myChart = new Chart(ctx, {
                type: tipe,
                data: {
                labels: request.map((item) => item.name),
                datasets: [
                    {
                    label: "Tendencia",
                    data: request.map((item) => item.count),
                    backgroundColor: dynamicColors,
                    minBarLength: 2,
                    },
                ],
                },
                options: {
                    scales: {
                        yAxes: [{
                            ticks: {
                                beginAtZero: true
                            }
                        }]
                    }
                }
            });
            // legends.innerHTML = myChart.generateLegend();
            },
        }
    }
</script>
