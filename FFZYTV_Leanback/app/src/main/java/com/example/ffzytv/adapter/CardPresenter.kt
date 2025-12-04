package com.example.ffzytv.adapter

import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.ImageView
import android.widget.TextView
import androidx.leanback.widget.Presenter
import coil.load
import com.example.ffzytv.R
import com.example.ffzytv.model.VodItem

class CardPresenter : Presenter() {

    override fun onCreateViewHolder(parent: ViewGroup): ViewHolder {
        val view = LayoutInflater.from(parent.context)
            .inflate(R.layout.item_card, parent, false)
        return ViewHolder(view)
    }

    override fun onBindViewHolder(viewHolder: ViewHolder, item: Any) {
        val vod = item as VodItem
        val imageView = viewHolder.view.findViewById<ImageView>(R.id.image)
        val titleView = viewHolder.view.findViewById<TextView>(R.id.title)
        val remarkView = viewHolder.view.findViewById<TextView>(R.id.remark)

        imageView.load(vod.pic) {
            placeholder(R.color.violet_500)
            error(R.color.gray_500)
        }
        titleView.text = vod.name
        remarkView.text = vod.remarks
    }

    override fun onUnbindViewHolder(viewHolder: ViewHolder) {}
}
