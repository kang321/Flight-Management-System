import React, { useState, useEffect } from "react";
import classes from "./SearchForm.module.css";

import Input from "../UI/Input/Input";
import axiosInstance from "../../axios";
import Spinner from "../UI/Spinner/spinner";
import Table from "../UI/Table/Table";
import Moment from "moment";
import Layout from "../Layout/Layout"; 

const AIRPORTS = [
	{
		india: [
            { value: "Source", displayValue: "Source" },
			{ value: "AMD", displayValue: "AMD - Ahmedabad" },
			{ value: "BLR", displayValue: "BLR - Banglore" },
			{ value: "IXC", displayValue: "IXC - Chandigarh" },
			{ value: "MAA", displayValue: "MAA - Chennai" },
			{ value: "DEL", displayValue: "DEL - Delhi" },
			{ value: "HYD", displayValue: "HYD - Hyderabad" },
			{ value: "COK", displayValue: "COK - Kochi" },
			{ value: "CCU", displayValue: "CCU - Kolkata" },
			{ value: "BOM", displayValue: "BOM - Mumbai" },
		],
		canada: [
            { value: "Destination", displayValue: "Destination" },
			{ value: "YYC", displayValue: "YYC - Calgary" },
			{ value: "YHZ", displayValue: "YHZ - Nova Scotia" },
			{ value: "YOW", displayValue: "YOW - Ottawa" },
			{ value: "YQB", displayValue: "YQB - Quebec" },
			{ value: "YYZ", displayValue: "YYZ - Toronto" },
			{ value: "YVR", displayValue: "YVR - Vancover" },
			{ value: "YWG", displayValue: "YWG - Winnipeg" },
		],
	},
];

const SearchForm = (props) => {
	const [state, setState] = useState({
		orderForm: {
			origin: {
				elementType: "select",
				elementConfig: {
					options: AIRPORTS,
				},
				value: "Source",
			},
			destination: {
				elementType: "select",
				elementConfig: {
					options: AIRPORTS,
				},
				value: "Destination",
			},
			date: {
				elementType: "date",
				value: new Date().toISOString().substring(0, 10),
			},
			number: {
				elementType: "number",
				value: 1,
			},
		},
		loading: false,
		live: false,
		cached: false,
	});

	const [data, setData] = useState();

	/////////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////////////////////////////////////////////////////

	const inputChangedHandler = (event, formElementIdentifier) => {
		// clone all input elements
		const updatedOrderForm = {
			...state.orderForm,
		};

		// clone the properties inside THIS input-element
		const updatedFormElement = {
			...updatedOrderForm[formElementIdentifier],
		};

		// Update THIS input-element's fields (if it's not dropdown)
		updatedFormElement.value = event.target.value;

		// Updated form for THIS input-element gets the updated input-element
		updatedOrderForm[formElementIdentifier] = updatedFormElement;

		setState({ orderForm: updatedOrderForm });
	};

	/////////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////////////////////////////////////////////////////

	const getPayload = () => {
		let payload = {
			source: state.orderForm.origin.value,
			destination: state.orderForm.destination.value,
			date: Moment(state.orderForm.date.value).format("YYYY-MM-DD"),
			person: state.orderForm.number.value,
		};

		return payload;
	};

    /////////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////////////////////////////////////////////////////

    const validate = () => {
        let payload = getPayload();
        if (payload.source == 'Source' || payload.destination == 'Destination') return false;
        return true;
    }

	/////////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////////////////////////////////////////////////////

	const searchLive = () => {

        if (!validate()) {
            alert("select correct source and destination airports");
            return;
        }

		let payload = getPayload();

		setState({ ...state, loading: true });

		axiosInstance.post("/site_open", payload).then((res) => {
			setState({ ...state, loading: false });
			setData(res.data);
		});
	};

	/////////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////////////////////////////////////////////////////

	const searchCached = () => {

        if (!validate()) {
            alert("select correct source and destination airports");
            return;
        }

		let payload = getPayload();

		setState({ ...state, loading: true });

		axiosInstance.post("/site_open/cache", payload).then((res) => {
			setState({ ...state, loading: false });
			setData(res.data);
		});
	};

	/////////////////////////////////////////////////////////////////////////////////////////
	/////////////////////////////////////////////////////////////////////////////////////////

	// create an array from the state
	const formElementsArray = [];
	for (let key in state.orderForm) {
		formElementsArray.push({
			id: key,
			config: state.orderForm[key],
		});
	}

    // get data for the table to be displayed
	let table = <></>;
	if (data && data.length > 0) {
		table = <Table flights={data} />;
	}

	// create a form with Input elements using info from the above array
	let form = (
		<>
			{formElementsArray.map((formElement) => {
				return (
					<Input
						key={formElement.id}
						changed={(event) => {
							inputChangedHandler(event, formElement.id);
						}}
						elementType={formElement.config.elementType}
						elementConfig={formElement.config.elementConfig}
						value={formElement.config.value}
					/>
				);
			})}
		</>
	);

	if (state.loading) form = <Spinner />;

	return (
		<div className={classes.background}>
			<Layout>
				<div className={classes.SearchForm}>
					<h4c className={classes.title}>Search ✈️</h4c>
					{form}
				</div>
				<div className={classes.buttons}>
					<button
						className={classes.TealButton}
						onClick={searchCached}>
						cached results
					</button>
					<button className={classes.Button} onClick={searchLive}>
						live results
					</button>
				</div>
				{table}
			</Layout>
		</div>
	);
};

export default SearchForm;
