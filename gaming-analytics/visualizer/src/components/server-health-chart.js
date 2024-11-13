// src/components/server-health-chart.js
import React, { useEffect, useRef } from 'react';
import ReactEcharts from 'echarts-for-react';

function ServerHealthChart({ data }) {
    const chartRef = useRef();

    const getOption = () => ({
        title: { text: 'Server Health Metrics' },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: data.map((d) => d.server_id) },
        yAxis: { type: 'value' },
        series: [
            {
                name: 'CPU Load',
                type: 'line',
                data: data.map((d) => d.cpu_load),
            },
            {
                name: 'Latency',
                type: 'line',
                data: data.map((d) => d.latency),
            },
        ]
    });

    return <ReactEcharts ref={chartRef} option={getOption()} style={{ height: 400, width: '100%' }} />;
}

export default ServerHealthChart;
