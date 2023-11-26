import { useState, useEffect } from "react";
import { Box, Stack, Typography } from "@mui/material";
import Videos from "./Videos";
import SideBar from "./SideBar";
import { videos_lists } from "../utils/sample";
import "./home.css";
import SearchBar from "./SearchBar";
import axios from "axios";
import Cookies from "js-cookie";
// import { fetchFromAPI } from "../utils/fetchFromAPI";

const Feed = () => {
  const [selectedCategory, setSelectedCategory] = useState(`New`);
  const videos_list = axios.get("address : http://localhost:8000/content/", {
    tag: "New",
    searchTerm: "",
    cookie:Cookies.get('user'),
    num: 20,
  }).then((res)=>(res.data));
  // const videos_list = videos_lists[selectedCategory]
  const [videos, setVideos] = useState(videos_list);
  useEffect(() => {
    document.body.style.backgroundColor = "#181818";
    import("./home.css");
    return () => {
      document.body.style.backgroundColor = null;
    };
  }, []);
  return (
    <div>
      <div>
        <SearchBar
          setVideos={setVideos}
          setSelectedCategory={setSelectedCategory}
        />
      </div>
      <Stack sx={{ flexDirection: { sx: "column", md: "row" } }}>
        <Box
          sx={{
            height: { sx: "auto", md: "92vh" },
            borderRight: "1px solid #3d3d3d",
            px: { sx: 0, md: 2 },
          }}
        >
          <SideBar
            selectedCategory={selectedCategory}
            setSelectedCategory={setSelectedCategory}
            setVideos={setVideos}
          />
        </Box>

        <Box p={2} sx={{ overflowY: "auto", height: "90vh", flex: 2 }}>
          <Typography
            variant="h4"
            fontWeight="bold"
            mb={2}
            sx={{ color: "white" }}
          >
            {selectedCategory}
          </Typography>
          <Videos videos={videos} selectedCategory={selectedCategory} />
        </Box>
      </Stack>
    </div>
  );
};

export default Feed;
