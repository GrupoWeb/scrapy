<?php

use Illuminate\Database\Seeder;
use App\statu;

class statusSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */
    public function run()
    {
        $status = new statu;
        $status->name = 'Activo';
        $status->save();

        $status = new statu;
        $status->name = 'Desactivo';
        $status->save();
        
    }
}
