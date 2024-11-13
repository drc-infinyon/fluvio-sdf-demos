// src/app.js
import React, { useState, useEffect } from 'react';
import EngagementChart from './components/engagement-chart';
import FraudDetectionChart from './components/fraud-detection-chart';
import ServerHealthChart from './components/server-health-chart';

function App() {
    const [engagementData, setEngagementData] = useState([]);
    const [fraudData, setFraudData] = useState([]);
    const [serverHealthData, setServerHealthData] = useState([]);

    useEffect(() => {
        const eventSource = new EventSource("http://localhost:8000/stream_events");

        eventSource.onmessage = function (event) {
            const data = JSON.parse(event.data);

            if (data.type === "engagement-metrics") {
                setEngagementData((prev) => [...prev, data]);
            } else if (data.type === "fraud-detections") {
                setFraudData((prev) => [...prev, data]);
            } else if (data.type === "server-health-metrics") {
                setServerHealthData((prev) => [...prev, data]);
            }
        };

        return () => {
            eventSource.close();
        };
    }, []);

    return (
        <div>
            <h1>Gaming Analytics Dashboard</h1>
            <EngagementChart data={engagementData} />
            <FraudDetectionChart data={fraudData} />
            <ServerHealthChart data={serverHealthData} />
        </div>
    );
}

export default App;
