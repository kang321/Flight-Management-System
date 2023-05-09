import React, { useState } from "react";
import classes from "./Table.module.css";

const Table = ({ flights }) => {
	const [state, setState] = useState({
		priceLow: structuredClone(flights),
		priceHigh: structuredClone(flights).sort((a, b) => b.CAD - a.CAD),
		durationLow: structuredClone(flights).sort((a, b) =>
			a.Duration.localeCompare(b.Duration)
		),
		durationHigh: structuredClone(flights).sort((a, b) =>
			b.Duration.localeCompare(a.Duration)
		),
		data: flights,
	});

	const handleSelect = (event) => {
		if (event.target.value == "priceLow")
			setState({ ...state, data: state.priceLow });
		else if (event.target.value == "priceHigh")
			setState({ ...state, data: state.priceHigh });
		else if (event.target.value == "durationLow")
			setState({ ...state, data: state.durationLow });
		else if (event.target.value == "durationHigh")
			setState({ ...state, data: state.durationHigh });
	};

	let rows = state.data.map((flight, idx) => {
		return (
			<tr key={idx}>
				<td>{flight.Airlines ? flight.Airlines : "-"}</td>
				<td>{flight.Source ? flight.Source : "-"}</td>
				<td>{flight.Destination ? flight.Destination : "-"}</td>
				<td>{flight.Date ? flight.Date : "-"}</td>
				<td>{flight.Departure_time ? flight.Departure_time : "-"}</td>
				<td>{flight.Arrival_time ? flight.Arrival_time : "-"}</td>
				<td>{flight.Stops ? flight.Stops : "-"}</td>
				<td>{flight.Duration ? flight.Duration : "-"}</td>
				<td>{flight.CAD ? "$" + flight.CAD : "-"}</td>
			</tr>
		);
	});

	return (
		<div className={classes.box}>
			<select
				value={state.value}
				onChange={handleSelect}
				className={classes.custom_select}>
				<option value='priceLow'>price low to high</option>
				<option value='priceHigh'>price high to low</option>
				<option value='durationLow'>duration low to high</option>
				<option value='durationHigh'>duration high to low</option>
			</select>
 
			<table className={classes.Table}>
				<thead>
					<tr>
						<th>Airlines</th>
						<th>Source</th>
						<th>Destination</th>
						<th>Date</th>
						<th>Departure Time</th>
						<th>Arrival Time</th>
						<th>Stops</th>
						<th>Duration</th>
						<th>Price</th>
					</tr>
				</thead>
				<tbody>{rows}</tbody>
			</table>
		</div>
	);
};

export default Table;
