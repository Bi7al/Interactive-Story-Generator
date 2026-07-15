import { useState,useEffect } from "react";



function StoryGame({story,onNewStory}){
    const [currentNodeId,setCurrentNodeId]=useState(null)

    const [currentNode,setCurrentNode]=useState(null)

    const [options,setOptions]=useState([])

    const [isEnding,setIsEnding]=useState(false)
    const [isWinning,setIsWinning]=useState(false)


    useEffect(()=>{
        if (story && story.root_node){
            const rootNodeId = story.root_node.id
            setCurrentNodeId(rootNodeId)
        }
    },[story])

    useEffect(()=>{
        if (currentNodeId && story && story.all_nodes){
            const node = story.all_nodes[currentNodeId]
            setCurrentNode(node)
            setIsEnding(node.is_ending)
            setIsWinning(node.is_winning)
            if (!node.is_ending && node.options && node.options.length >0){
                setOptions(node.options)
            }else{
                setOptions([])
            }
        }
    },[currentNodeId,story])

    function choseOption(optionId){
        setCurrentNodeId(optionId)
    }
    function restartStory(){
        if(story && story.root_node){
            setCurrentNodeId(story.root_node.id)
        }
    }



    return(
        <div className="story-game">
            <header className="story-header">
                <h2>{story.title}</h2>
            </header>
            <div className="story-content">
                {
                    currentNode && <div className="story-node">
                        <p>{currentNode.content}</p>
                    </div>
}

                    {
                        isEnding ? <div className="story-ending">
                            <h3>{isWinning ? "Congragulations": "The End"}</h3>
                            {isWinning?"You Reached a Winning Ending":"Your Adventure has Come to an End"}
                        </div>: <div className="story-options">
                            <h3>What Will You Do ?</h3>
                            <div className="options-list">
                                {options.map((option,ind)=>{
                                    return <button key={ind} onClick={()=>{choseOption(option.node_id)}}
                                    className="option-btn">
                                        {option.text}
                                    </button>
                                })
                                }
                            </div>
                        </div>

                    }
                
            </div>
            <div className="story-controls">
                <button onClick={restartStory} className="reset-btn">Restart Story</button>

            </div>
            {onNewStory && <button className="new-story-btn" onClick={onNewStory}>New Story</button>}
        </div>
    )
}


export default StoryGame