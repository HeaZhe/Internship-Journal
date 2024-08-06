import { BrowserRouter, Routes, Route, Navigate} from "react-router-dom"
import Stocks from "./pages/Stocks"
import News from "./pages/News"
import NewsDetail from "./pages/NewsDetail"
import NTUT_Posts from "./pages/NTUT_Posts"


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/news" element={<News />} />
        <Route path="/news/:id" element={<NewsDetail />} />
        <Route path="/stocks" element={<Stocks />} />
        <Route path="/ntut_posts" element={<NTUT_Posts />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App
