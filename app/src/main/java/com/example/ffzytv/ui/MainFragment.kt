package com.example.ffzytv.ui

import android.content.Intent
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import androidx.core.content.ContextCompat
import androidx.leanback.app.BackgroundManager
import androidx.leanback.app.BrowseSupportFragment
import androidx.leanback.widget.*
import com.example.ffzytv.R
import com.example.ffzytv.adapter.CardPresenter
import com.example.ffzytv.model.VodItem
import com.example.ffzytv.network.ApiClient

class MainFragment : BrowseSupportFragment() {

    private lateinit var backgroundManager: BackgroundManager
    private val categories = listOf(
        Pair(36, "短剧"),
        Pair(22, "日剧"),
        Pair(13, "韩剧"),
        Pair(15, "美剧"),
        Pair(6, "国产剧")
    )

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setupUI()
        loadRows()
    }

    private fun setupUI() {
        title = getString(R.string.app_name)
        isHeadersStateHidden = false
        setBadgeDrawable(ContextCompat.getDrawable(requireActivity(), R.drawable.app_icon))

        backgroundManager = BackgroundManager.getInstance(activity)
        backgroundManager.attach(window)
        backgroundManager.setBitmap(null)

        setOnSearchClickedListener {
            startActivity(Intent(activity, SearchActivity::class.java))
        }
    }

    private fun loadRows() {
        val rowsAdapter = ArrayObjectAdapter(ListRowPresenter())

        categories.forEach { (typeId, name) ->
            val listRowAdapter = ArrayObjectAdapter(CardPresenter()) { item ->
                val vod = item as VodItem
                PlayerActivity.start(requireContext(), vod)
            }

            ApiClient.instance.getList(typeId = typeId, page = 1).enqueue(object :
                retrofit2.Callback<com.example.ffzytv.model.ApiResponse> {
                override fun onResponse(
                    call: retrofit2.Call<com.example.ffzytv.model.ApiResponse>,
                    response: retrofit2.Response<com.example.ffzytv.model.ApiResponse>
                ) {
                    if (response.isSuccessful) {
                        Handler(Looper.getMainLooper()).post {
                            response.body()?.list?.forEach { vod ->
                                listRowAdapter.add(vod)
                            }
                            rowsAdapter.add(ListRow(HeaderItem(name), listRowAdapter))
                        }
                    }
                }

                override fun onFailure(call: retrofit2.Call<com.example.ffzytv.model.ApiResponse>, t: Throwable) {}
            })
        }

        adapter = rowsAdapter
    }
}
