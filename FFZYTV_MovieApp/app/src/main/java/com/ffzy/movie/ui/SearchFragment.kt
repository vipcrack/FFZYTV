package com.ffzy.movie.ui
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.leanback.app.SearchSupportFragment
import androidx.leanback.widget.*
import com.ffzy.movie.adapter.CardPresenter
import com.ffzy.movie.model.VodItem
import com.ffzy.movie.network.ApiClient
class SearchFragment : SearchSupportFragment() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setSearchResultProvider(object : SearchResultProvider {
            override fun getResults(query: String?): MutableList<Any> = mutableListOf()
            override fun onQueryTextChange(newQuery: String?): Boolean {
                if (!newQuery.isNullOrBlank()) search(newQuery)
                return true
            }
            override fun onQueryTextSubmit(query: String?): Boolean {
                if (!query.isNullOrBlank()) search(query)
                return true
            }
        })
    }
    private fun search(keyword: String) {
        val adapter = ArrayObjectAdapter(ListRowPresenter())
        ApiClient.service.search(wd = keyword, pg = 1).enqueue { _, response ->
            if (response.isSuccessful) {
                Handler(Looper.getMainLooper()).post {
                    val cardAdapter = ArrayObjectAdapter(CardPresenter()) { item ->
                        PlayerActivity.start(requireContext(), item as VodItem)
                    }
                    response.body()?.list?.forEach { cardAdapter.add(it) }
                    adapter.add(ListRow(HeaderItem("搜索 "$keyword""), cardAdapter))
                    this.adapter = adapter
                }
            }
        }
    }
}
