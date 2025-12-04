package com.example.ffzytv.ui

import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.leanback.app.SearchSupportFragment
import androidx.leanback.widget.ArrayObjectAdapter
import androidx.leanback.widget.HeaderItem
import androidx.leanback.widget.ListRow
import androidx.leanback.widget.ListRowPresenter
import com.example.ffzytv.adapter.CardPresenter
import com.example.ffzytv.model.VodItem
import com.example.ffzytv.network.ApiClient
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class SearchFragment : SearchSupportFragment() {

    private lateinit var rowsAdapter: ArrayObjectAdapter

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setSearchResultProvider(object : SearchSupportFragment.SearchResultProvider {
            override fun getResults(searchQuery: String?): MutableList<Any> = mutableListOf()

            override fun onQueryTextChange(newQuery: String?): Boolean {
                if (!newQuery.isNullOrBlank()) search(newQuery.trim())
                return true
            }

            override fun onQueryTextSubmit(query: String?): Boolean {
                if (!query.isNullOrBlank()) search(query.trim())
                return true
            }
        })

        rowsAdapter = ArrayObjectAdapter(ListRowPresenter())
        adapter = rowsAdapter
    }

    private fun search(keyword: String) {
        rowsAdapter.clear()

        ApiClient.instance.getList(ac = "search", wd = keyword, pg = 1).enqueue(object :
            Callback<com.example.ffzytv.model.ApiResponse> {
            override fun onResponse(
                call: Call<com.example.ffzytv.model.ApiResponse>,
                response: Response<com.example.ffzytv.model.ApiResponse>
            ) {
                if (response.isSuccessful) {
                    Handler(Looper.getMainLooper()).post {
                        val list = response.body()?.list ?: emptyList()
                        if (list.isNotEmpty()) {
                            val cardAdapter = ArrayObjectAdapter(CardPresenter()) { item ->
                                val vod = item as VodItem
                                PlayerActivity.start(requireContext(), vod)
                            }
                            list.forEach { cardAdapter.add(it) }
                            rowsAdapter.add(ListRow(HeaderItem("搜索结果 "$keyword""), cardAdapter))
                        }
                    }
                }
            }

            override fun onFailure(call: Call<com.example.ffzytv.model.ApiResponse>, t: Throwable) {}
        })
    }
}
