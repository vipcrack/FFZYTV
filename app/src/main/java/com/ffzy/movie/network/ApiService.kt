package com.ffzy.movie.network
import com.ffzy.movie.model.ApiResponse
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Query
interface ApiService {
    @GET("api.php/provide/vod/")
    fun getMovies(@Query("t") t: Int, @Query("pg") pg: Int): Call<ApiResponse>
    @GET("api.php/provide/vod/")
    fun search(@Query("wd") wd: String, @Query("pg") pg: Int): Call<ApiResponse>
}
