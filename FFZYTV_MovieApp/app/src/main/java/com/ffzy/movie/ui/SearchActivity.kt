package com.ffzy.movie.ui
import android.os.Bundle
import androidx.fragment.app.FragmentActivity
class SearchActivity : FragmentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        supportFragmentManager.beginTransaction()
            .replace(android.R.id.content, SearchFragment()).commit()
    }
}
