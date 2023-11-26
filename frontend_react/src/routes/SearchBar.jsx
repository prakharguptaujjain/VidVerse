import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Paper, IconButton } from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import axios from "axios";
import { videos_lists } from "../utils/sample";

const SearchBar = ({ setVideos, setSelectedCategory }) => {
  const [searchTerm, setSearchTerm] = useState("");

  const onhandleSubmit = (e) => {
    e.preventDefault();
    setSelectedCategory('Search')
    setVideos(
      // axios
      //   .get("address : http://localhost:8000/content/", {
      //     tag: "Search",
      //     searchTerm: searchTerm,
      //     num: 20,
      //   })
      //   .then((res) => res.data)
      videos_lists['Search']
    );
  };

  return (
    <Paper
      component="form"
      onSubmit={onhandleSubmit}
      sx={{
        borderRadius: 20,
        border: "1px solid #e3e3e3",
        pl: 2,
        boxShadow: "none",
        mr: { sm: 0 },
      }}
    >
      <input
        className="search-bar"
        placeholder="Search..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
      />
      <IconButton
        type="submit"
        sx={{ p: "10px", color: "red" }}
        aria-label="search"
      >
        <SearchIcon />
      </IconButton>
    </Paper>
  );
};

export default SearchBar;