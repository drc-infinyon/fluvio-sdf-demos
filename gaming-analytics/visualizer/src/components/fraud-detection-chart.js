// src/components/fraud-detection-chart.js
import React, { useEffect, useRef } from 'react';
import ReactEcharts from 'echarts-for-react';

function FraudDetectionChart({ data }) {
    const chartRef = useRef();

    const getOption = () => ({
        title: { text: 'Fraud Detection' },
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: data.map((d) => d.user_id) },
        yAxis: { type: 'value' },
        series: [{
            name: 'Suspicious Purchases',
            type: 'line',
            data: data.map((d) => d.suspicious_purchase_count),
        }]
    });

    return <ReactEcharts ref={chartRef} option={getOption()} style={{ height: 400, width: '100%' }} />;
}

export default FraudDetectionChart;
