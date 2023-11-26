import { Stack, Box } from "@mui/material";
import VideoCard from "./VideoCard";
import ChannelCard from "./ChannelCard";
import Loader from "./Loader.jsx";
import {
  Line,
  LineChart,
  ResponsiveContainer,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";
import { chartData } from "../utils/sample.js";
import axios from "axios";
import Cookies from "js-cookie";

const Videos = ({ videos, selectedCategory }) => {
  if (selectedCategory != "Dashboard" && selectedCategory != "Ads") {
    if (!videos?.length) return <Loader />;
    return (
      <Stack direction={"row"} flexWrap="Wrap" justifyContent="start" gap={2}>
        {videos.map((item, idx) => (
          <Box key={idx}>{item.vid && <VideoCard video={item} />}</Box>
        ))}
      </Stack>
    );
  } else if (selectedCategory == "Dashboard") {
    const data = axios
      .get("http://localhost:8000/creator/", { cookie: Cookies.get("user") })
      .then((res) => res.data);
    return (
      <div>
        <div className="infoContainer">
          <div className="info">
            <h2>Liked</h2>
            <h4>{data.liked}</h4>
          </div>
          <div className="info">
            <h2>Watch Time</h2>
            <h4>{data.watchTime}</h4>
          </div>
          <div className="info">
            <h2>Views</h2>
            <h4>{data.views}</h4>
          </div>
        </div>
        <div className="chart">
          <LineChart width={1200} height={400} data={data.chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" stroke="#ffffff" />
            <YAxis stroke="#ffffff" />
            <Line type="monotone" dataKey="views" stroke="#ffffff" />
          </LineChart>
        </div>
      </div>
    );
  } else if (selectedCategory == "Ads") {
    const data = axios
      .get("http://localhost:8000/advertiser/", { cookie: Cookies.get("user") })
      .then((res) => res.data);
    return (
      <div>
        <div className="infoContainer">
          <div className="info">
            <h2>Ads Shown</h2>
            <h4>{data.adShown }</h4>
          </div>
          <div className="info">
            <h2>Ads Clicked</h2>
            <h4>{data.adsClicked }</h4>
          </div>
          <div className="info">
            <h2>BackLinking</h2>
            <h4>{data.backLinking }</h4>
          </div>
        </div>
        <div className="chart">
          <LineChart width={1200} height={400} data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="date" stroke="#ffffff" />
            <YAxis stroke="#ffffff" />
            <Line type="monotone" dataKey="clicked" stroke="#ffffff" />
          </LineChart>
        </div>
      </div>
    );
  }
};

export default Videos;
