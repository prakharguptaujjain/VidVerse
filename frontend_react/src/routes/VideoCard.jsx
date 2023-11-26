import { Link } from 'react-router-dom';
import { Typography, Card, CardContent, CardMedia } from '@mui/material';
import { CheckCircle } from '@mui/icons-material';
import { demoThumbnailUrl, demoVideoUrl, demoVideoTitle, demoChannelUrl, demoChannelTitle } from '../utils/constants';



const VideoCard = ({ video }) => {
  return (
    <Card sx={{ width:{ md: '300px', xs: '100%' },
    boxShadow: 'none' , borderRadius: '0' }}>
        <Link to = {video.vid ? `/video/${video.vid}` : demoVideoUrl}>
        <CardMedia image={video.thumbnails}
        alt= {video.title}
        // sx = {{ width: 358, height: 180 }}
        sx = {{ width: '100%', height: 180 }}
         />
        </Link>
        <CardContent sx={{ backgroundColor: '#1e1e1e',
        height: '106px' }} >
          <Link to = {video.vid ? `/video/${video.vid}` : demoVideoUrl}>
            <Typography variant="subtitle1"
            fontWeight="bold" color="#FFF" >
              {video.title.slice(0, 60) || demoVideoTitle.slice(0, 60)}
            </Typography>
          </Link>
        </CardContent>
    </Card>
  )
}

export default VideoCard