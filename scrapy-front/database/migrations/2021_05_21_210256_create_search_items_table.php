<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateSearchItemsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('search_items', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->bigInteger('master_id')->unsigned();
            $table->bigInteger('categories_id')->unsigned();
            $table->bigInteger('products_id')->unsigned();
            $table->bigInteger('status_id')->unsigned();

            $table->timestamps();

            $table->foreign('master_id')->references('id')->on('search_masters');
            $table->foreign('categories_id')->references('id')->on('categories');
            $table->foreign('products_id')->references('id')->on('products');
            $table->foreign('status_id')->references('id')->on('status');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('search_items');
    }
}
