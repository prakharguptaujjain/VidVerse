import { Stack } from "@mui/material";
import { Link } from "react-router-dom";

const Suggestion = ({ suggestionList }) => (
  <Stack
    direction="Row"
    sx={{
      overflowY: "auto",
      height: { sx: "auto", md: "95%" },
      flexDirection: { md: "column" },
    }}
  >
    <h3 className="videoTitle">Recommendation</h3>
    {suggestionList.map((Suggestion) => (
        <Link to={`/video/${Suggestion.vid}`}>
        <div>
          <h4 style={{ color: "white" }}>
            {Suggestion.title}
          </h4>
        </div>
      </Link>
    ))}
  </Stack>
);

export default Suggestion;
