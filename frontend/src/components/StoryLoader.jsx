import { useState, useEffect } from "react";
import { useParams,useNavigate } from "react-router-dom";
import axios from "axios";
import LoadingStatus from "./LoadingStatus.jsx";
import StoryGame from "./StoryGame.jsx";
import { API_BASE_URL } from "../../util.js";

function StoryLoader(){
    const {id} = useParams()
    
    const navigate=useNavigate()
    const [story,setStory]=useState(null)
    const [loading,setLoading]=useState(true)
    const [error,setError]=useState(null)



    async function loadStory(storyId){
        
        setLoading(true)
        setError(null)
        try{
            
            
            const response = await axios.get(`${import.meta.env.BACKEND_URL}/${API_BASE_URL}/stories/${storyId}/complete`)
            
            setStory(response.data)
            
        }catch(error){
            if (error.response?.status ===404){
                setError("Story Not Found")
            }
            else{
                setError("Failed to load Story")
            }
        }finally{
            setLoading(false)
        }
    }
        useEffect(()=>{
            if(id){
            loadStory(id)
        }
        },[id])

        const createNewStroy=()=>{
            navigate("/")
        }
        if (loading){
            return <LoadingStatus theme={"story"} />
        }

        if(error){
            return(
                <div className="story-loader">
                    <div className="error-message">
                        <h2>Story not Found</h2>
                        <p>{error}</p>
                        <button onClick={createNewStroy}>Go to story Generator</button>
                    </div>
                </div>
            )
        }

        if(story){
            return(
                <div className="story-loader">
                    <StoryGame story={story} onNewStory={createNewStroy}/>
                </div>
            )
        }
    



    
}
export default StoryLoader