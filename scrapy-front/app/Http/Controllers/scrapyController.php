<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

class scrapyController extends Controller
{
    public function index(){
        return view('auth.login');
    }

    public function home(){
        return view('home');
    }

    public function lista(){
        return view('scrapy.lista');
    }

    public function categories(){
        return view('scrapy.categories');
    }

    public function products(){
        return view('scrapy.products');
    }

    public function search(){
        return view('scrapy.search');
    }

    public function intelligence(){
        return view ('scrapy.intelligence');
    }

}
