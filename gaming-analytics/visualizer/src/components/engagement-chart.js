// src/components/engagement-chart.js
import React, { useEffect, useRef } from 'react';
import ReactEcharts from 'echarts-for-react';

function EngagementChart({ data }) {
    const chartRef = useRef();

    const getOption = () => ({
        title: { text: 'Player Engagement by Level and Map' },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: data.map((d) => `${d.level_id}-${d.map_id}`) },
        yAxis: { type: 'value' },
        series: [{
            name: 'Active Players',
            type: 'bar',
            data: data.map((d) => d.active_players),
        }]
    });

    return <ReactEcharts ref={chartRef} option={getOption()} style={{ height: 400, width: '100%' }} />;
}

export default EngagementChart;
