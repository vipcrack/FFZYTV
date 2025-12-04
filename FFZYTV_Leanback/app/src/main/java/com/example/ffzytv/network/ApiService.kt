package com.example.ffzytv.network

import com.example.ffzytv.model.ApiResponse
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Query

interface ApiService {
    @GET("api.php/provide/vod/")
    fun getList(
        @Query("ac") ac: String = "list",
        @Query("t") typeId: Int? = null,
        @Query("pg") page: Int = 1,
        @Query("wd") keyword: String? = null
    ): Call<ApiResponse>

    @GET("api.php/provide/vod/")
    fun getDetail(@Query("ids") id: Int): Call<ApiResponse>
}
