package com.ffzy.movie.ui
import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.leanback.app.BrowseSupportFragment
import androidx.leanback.widget.*
import com.ffzy.movie.R
import com.ffzy.movie.adapter.CardPresenter
import com.ffzy.movie.model.VodItem
import com.ffzy.movie.network.ApiClient
class MainFragment : BrowseSupportFragment() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        title = "电影"
        isHeadersStateHidden = true
        setOnSearchClickedListener { startActivity(Intent(activity, SearchActivity::class.java)) }
        loadMovies()
    }
    private fun loadMovies() {
        val rowAdapter = ArrayObjectAdapter(CardPresenter()) { item ->
            PlayerActivity.start(requireContext(), item as VodItem)
        }
        val rowsAdapter = ArrayObjectAdapter(ListRowPresenter())
        ApiClient.service.getMovies(t = 1, pg = 1).enqueue(object : retrofit2.Callback<com.ffzy.movie.model.ApiResponse> {
            override fun onResponse(call: retrofit2.Call<com.ffzy.movie.model.ApiResponse>, response: retrofit2.Response<com.ffzy.movie.model.ApiResponse>) {
                if (response.isSuccessful) {
                    Handler(Looper.getMainLooper()).post {
                        response.body()?.list?.forEach { rowAdapter.add(it) }
                        rowsAdapter.add(ListRow(null, rowAdapter))
                        adapter = rowsAdapter
                    }
                }
            }
            override fun onFailure(call: retrofit2.Call<com.ffzy.movie.model.ApiResponse>, t: Throwable) {}
        })
    }
}
