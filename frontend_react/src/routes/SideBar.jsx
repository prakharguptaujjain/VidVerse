import { Stack } from "@mui/material";
import { categories } from "../utils/constants";
import axios from "axios";
import { videos_lists } from "../utils/sample";
import Cookies from "js-cookie";
const SideBar = ({ selectedCategory, setSelectedCategory, setVideos }) => (
  <Stack
    direction="Row"
    sx={{
      overflowY: "auto",
      height: { sx: "auto", md: "95%" },
      flexDirection: { md: "column" },
    }}
  >
    {categories.map((category) => (
      <button
        className="category-btn"
        onClick={() => {
          setSelectedCategory(category.name);
          if (category.name != "Search" && category.name != "Dashboard" && category.name != "Ads")
            setVideos(
              axios
                .get("address : http://localhost:8000/content/", {
                  tag: category.name,
                  searchTerm: "",
                  cookie:Cookies.get('user'),
                  num: 20,
                })
                .then((res) => res.data)
            );
            // setVideos(videos_lists[category.name]);
        }}
        style={{
          background: category.name === selectedCategory && "#FC1503",
          color: "white",
        }}
        key={category.name}
      >
        <span
          style={{
            color: category.name === selectedCategory ? "white" : "red",
            marginRight: "15px",
          }}
        >
          {category.icon}
        </span>
        <span
          style={{ opacity: category.name === selectedCategory ? "1" : "0.8" }}
        >
          {category.name}
        </span>
      </button>
    ))}
  </Stack>
);

export default SideBar;
