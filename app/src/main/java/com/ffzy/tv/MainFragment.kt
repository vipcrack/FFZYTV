package com.ffzy.tv

import android.content.Intent
import android.os.Bundle
import androidx.leanback.app.BrowseSupportFragment
import androidx.leanback.widget.*
import androidx.core.content.ContextCompat

class MainFragment : BrowseSupportFragment() {

    override fun onActivityCreated(savedInstanceState: Bundle?) {
        super.onActivityCreated(savedInstanceState)

        title = getString(R.string.app_name)
        headersState = HEADERS_ENABLED
        isHeadersTransitionOnBackEnabled = true
        brandColor = ContextCompat.getColor(requireContext(), R.color.fastlane_background)
        badgeDrawable = ContextCompat.getDrawable(requireContext(), R.drawable.banner)

        setupUi()
        loadRows()
    }

    private fun setupUi() {
        val presenter = CardPresenter()
        val listRowAdapter = ArrayObjectAdapter(ListRowPresenter())
        val cardList = mutableListOf<Movie>()

        // 示例视频
        cardList.add(Movie("示例影片", "这是一部测试影片", "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"))

        val rowAdapter = ArrayObjectAdapter(presenter)
        cardList.forEach { rowAdapter.add(it) }
        val header = HeaderItem(0, "推荐内容")
        listRowAdapter.add(ListRow(header, rowAdapter))

        adapter = listRowAdapter
    }

    override fun onItemClicked(itemViewHolder: Presenter.ViewHolder?, item: Any?, rowViewHolder: RowPresenter.ViewHolder?, row: Row?) {
        if (item is Movie) {
            val intent = Intent(activity, PlayerActivity::class.java).apply {
                putExtra(PlayerActivity.VIDEO_URL_EXTRA, item.videoUrl)
                putExtra(PlayerActivity.VIDEO_TITLE_EXTRA, item.title)
            }
            startActivity(intent)
        }
    }

    data class Movie(val title: String, val description: String, val videoUrl: String)

    class CardPresenter : Presenter() {
        override fun onCreateViewHolder(parent: ViewGroup): ViewHolder {
            val cardView = ImageCardView(parent.context).apply {
                isFocusable = true
                isFocusableInTouchMode = true
            }
            return ViewHolder(cardView)
        }

        override fun onBindViewHolder(viewHolder: ViewHolder, item: Any) {
            if (item is Movie) {
                (viewHolder.view as ImageCardView).apply {
                    titleText = item.title
                    contentText = item.description
                    setMainImageDimensions(312, 176)
                }
            }
        }

        override fun onUnbindViewHolder(viewHolder: ViewHolder) {}
    }
}
