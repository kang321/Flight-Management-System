import React from "react";
import classes from "./NavigationItems.module.css";
import NavigationItem from "./NavigationItem/NavigationItem";

const NavigationItems = () => (
	<ul className={classes.NavigationItems}>
		<NavigationItem link="/">Home</NavigationItem>
        <NavigationItem link="/search">Search Flights</NavigationItem>
	</ul>
);

export default NavigationItems;
