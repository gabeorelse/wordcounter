import * as d3 from "d3";

function pieData(chartData) {
    const width = 300;
    const height = 300;

    const svg = d3.select('#user_graph').append('svg')
    .attr('width', width)
    .attr('height', height)
    .append("g")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const pie = d3.pie().value(d => d.value);
    const arcs = pie(chartData);

    const arc = d3.arc()
        .innerRadius(0)
        .outerRadius(100);

    svg.selectAll("path")
    .data(pie(arcs))
    .enter().append("path")
    .attr("d", arc)
    .attr("fill", (_, i) => color(i));
}


async function getGraph() {
    const options = {
        method: 'GET',
        credentials: 'include',
        mode: 'cors',
        headers: {
            'Accept': 'application/json'
          }
    };
    try {
        console.log('Fetch request starting...');
        const userId = sessionStorage.getItem("user_id");
        const response = await fetch(`http://localhost:5000/user_home?user_id=${userId}`, options);
        if (!response.ok) {
            const err = await response.json();
            console.log("Is this working?");
            throw new Error (err.error);
        }
        const data = await response.json();
        if (data.success) {
            console.log('Graph retrieved');
            pieData(data.chartData);
        } 
    } catch (error) {
        console.error('Error:', error.message);
    }
}

getGraph();

