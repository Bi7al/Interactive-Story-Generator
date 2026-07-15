import { useState,useEffect  } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import ThemeInput from "./ThemeInput.jsx";
import LoadingStatus from "./LoadingStatus.jsx";
import { API_BASE_URL } from "../../util.js";



function StoryGenerator(){
    const navigate = useNavigate();
    const [theme,setTheme]=useState("");
    const [jobId,setJobId]=useState(null)
    const [jobStatus,setJobStatus]=useState(null)
    const [error,setError]=useState(false)
    const [loading,setLoading]=useState(false)


    



    async function generateStory(theme){
        setLoading(true)
        setError(null)
        setTheme(theme)
        try {
            const response = await axios.post(`${import.meta.env.VITE_BACKEND_URL}/${API_BASE_URL}/stories/create`,{theme})
            const {job_id,status}= response.data
            setJobId(job_id)
            setJobStatus(status)
            pollJobStatus(job_id)

        } catch (error) {
            setLoading(false)
            setError(`Failed To generate story:${error.message}`)
        }
    }


    async function pollJobStatus(jobId){
        try {
            const response = await axios.get(`${import.meta.env.VITE_BACKEND_URL}/${API_BASE_URL}/jobs/${jobId}`)
            const {status,story_id,error:jobError} = response.data
            setJobStatus(status)
            if(status == "completed" && story_id){
                fetchStory(story_id)
            }else if(status=='failed' || jobError){
                setError(jobError || "Failed to load story")
                setLoading(false)

            }

        } catch (error) {
            setError(`Failed to Check Job Status:${error.message}`)
            setLoading(false)
        }
    }

    async function fetchStory(storyId){

        try {
            setLoading(false)
            setJobStatus("Completed")
            navigate(`/story/${storyId}`)
        } catch (error) {
            setError(`Failed to Load Story. ${error.message}`)
            setLoading(false)
        }
   }

    function reset(){
        setError(false)
        setJobId(null)
        setJobStatus(null)
        setTheme("")
    }




    useEffect(()=>{

        let pollInterval;

        if (jobId && jobStatus === "processing"){
            pollInterval = setInterval(()=>{pollJobStatus(jobId)},5000)
        }

        return ()=>{
            if(pollInterval){
                clearInterval(pollInterval)
            }
        }
    },[jobId,jobStatus])








    return(
        <div className="story-generator">
            {error && 
                <div className="error-message">
                    <p>{error}</p>
                    <button onClick={reset}>Try Again</button>
                </div>            
            }


            {!jobId && !error && !loading &&
            <ThemeInput onSubmit={generateStory}/>}

            {loading && <LoadingStatus  theme={theme}/>}
        </div>
    )







}

export default StoryGenerator