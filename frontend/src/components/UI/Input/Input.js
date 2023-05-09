import React from "react";
import classes from "./Input.module.css";

let getOptions = (airports) => {
	let res = (
		<>
			<optgroup label='India'>
				{airports.india.map((elem, i) => {
					return (
						<option key={i} value={elem.value}>
							{elem.displayValue}
						</option>
					);
				})}
			</optgroup>
			<optgroup label='Canada'>
				{airports.canada.map((elem, i) => {
					return (
						<option key={i} value={elem.value}>
							{elem.displayValue}
						</option>
					);
				})}
			</optgroup>
		</>
	);

	return res;
};

const Input = (props) => {
	let inputElement = null;
	const inputClasses = [classes.InputElement];

	switch (props.elementType) {
		case "date":
			inputElement = (
				<input
					className={inputClasses.join(" ")}
					type='date'
					value={props.value}
					onChange={props.changed}
				/>
			);
			break;
		case "select":
			inputElement = (
				<select
					className={inputClasses.join(" ")}
					value={props.value}
                    isDisabled={props.value == 'Source' || props.value == 'Destination'}
					onChange={props.changed}>
					{props.elementConfig.options.map((airports) =>
						getOptions(airports)
					)}
				</select>
			);
			break;
		case "number":
			inputElement = (
				<input
					type='number'
					className={inputClasses.join(" ")}
					value={props.value}
					onChange={props.changed}
					min={0}
					defaultValue={1}
				/>
			);
			break;
	}

	return (
		<div className={classes.Input}>
			<label className={classes.Label}>{props.Label}</label>
			{inputElement}
		</div>
	);
};

export default Input;
