<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/','scrapyController@index');

Auth::routes();

Route::get('dashboard','scrapyController@home');

Route::get('lista','scrapyController@lista')->name('lista');
Route::get('categorias','scrapyController@categories')->name('categorias');
Route::get('productos','scrapyController@products')->name('productos');
Route::get('busqueda','scrapyController@search')->name('busqueda');
Route::get('inteligencia','scrapyController@intelligence')->name('inteligencia');
