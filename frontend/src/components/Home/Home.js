import React from "react";
import classes from "./Home.module.css";
import Layout from "../Layout/Layout";
import NavigationItem from "../Navigation/NavigationItems/NavigationItem/NavigationItem";

const Home = () => {
	return (
		<Layout>
			<div className={classes.box}>
				<h1 className={classes.title}>
					flight search <em>streamlined</em>
				</h1>
				<p className={classes.info}>Overwhelmed with flight options?</p>
				<p className={classes.info}>
					Want one place to see all search tools' results?
				</p>
				<p className={classes.info}>
					Use our tool to get <strong>unbiased, aggregated</strong> data
				</p>
                <a className={classes.link} href="/search">✈️ now!</a>
			</div>
            <img className={classes.image} src="https://images.unsplash.com/photo-1505870000807-1481b8924f11?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1170&q=80">
            </img>
		</Layout>
	);
};

export default Home;
