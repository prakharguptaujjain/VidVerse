import React, { useState, useEffect } from "react";
import "./video_player.css";
import { Box, Stack, Typography } from "@mui/material";
import Suggestion from "./Suggestion";
import data from "../utils/suggestion.json";
import { useParams } from "react-router-dom";
import ThumbUpIcon from "@mui/icons-material/ThumbUp";
import Comments from "./Comments";
import ThumbDownIcon from "@mui/icons-material/ThumbDown";
import axios from "axios";
import { video_details } from "../utils/sample";

export default function VideoPlayer() {
  const {vid} = useParams();
  // const data = axios
  //   .get("http://localhost:8000/video/", { vid: vid
//     cookie:Cookies.get('user'),})
  //   .then((res) => res.data);
  const data = video_details[vid]
  const currVideo = data.src
  const title = data.title
  const suggestion = data.recommandation;
  const comment = data.comments
  return (
    <div className="videoPlayerBody">
      <Stack sx={{ flexDirection: { sx: "column", md: "row" } }}>
        <div className="videoContainer">
          <video src={currVideo} width="100%" height="100%" controls></video>
          <span className="videoTitle">{title}</span>
          <button className="likeButton">
            <span>
              {" "}
              <ThumbUpIcon />
            </span>
          </button>
          <button className="likeButton">
            <span>
              {" "}
              <ThumbDownIcon/>
            </span>
          </button>
          <p></p>
          <h3 className="videoTitle">Comments</h3>
          <Comments commentList={comment} />
        </div>
        <Suggestion suggestionList={suggestion} />
      </Stack>
    </div>
  );
}
