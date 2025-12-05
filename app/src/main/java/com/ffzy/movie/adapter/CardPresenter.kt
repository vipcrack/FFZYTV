package com.ffzy.movie.adapter
import android.view.LayoutInflater
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.leanback.widget.Presenter
import coil.load
import com.ffzy.movie.R
import com.ffzy.movie.model.VodItem
class CardPresenter : Presenter() {
    override fun onCreateViewHolder(parent: ViewGroup): androidx.leanback.widget.Presenter.ViewHolder {
        val v = LayoutInflater.from(parent.context).inflate(R.layout.item_card, parent, false)
        return androidx.leanback.widget.Presenter.ViewHolder(v)
    }
    override fun onBindViewHolder(vh: androidx.leanback.widget.Presenter.ViewHolder, item: Any) {
        val vod = item as VodItem
        vh.view.findViewById<ImageView>(R.id.image).load(vod.pic)
        vh.view.findViewById<TextView>(R.id.title).text = vod.name
        vh.view.findViewById<TextView>(R.id.remark).text = vod.remarks
    }
    override fun onUnbindViewHolder(vh: androidx.leanback.widget.Presenter.ViewHolder) {}
}
