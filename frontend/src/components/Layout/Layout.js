import React, { Component } from "react";
import classes from "./Layout.module.css";
import Toolbar from "../../components/Navigation/Toolbar/Toolbar";
import SideDrawer from "../Navigation/SideDrawer/SideDrawer";

class Layout extends Component {
	state = {
		showSideDrawer: false,
	};

	//////////////////////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////////////////////

	sideDrawerCloser = () => {
		this.setState({ showSideDrawer: false });
	};

	//////////////////////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////////////////////

	sideDrawerToggler = () => {
		this.setState((prevState) => {
			return { showSideDrawer: !prevState.showSideDrawer };
		});
	};

	//////////////////////////////////////////////////////////////////////////////////////
	//////////////////////////////////////////////////////////////////////////////////////

	render() {
		return (
			<div className={classes.box}>
				<Toolbar toggler={this.sideDrawerToggler} />
				<SideDrawer
					drawerStatus={this.state.showSideDrawer}
					closed={this.sideDrawerCloser}
				/>
				<main className={classes.Content}>{this.props.children}</main>
			</div>
		);
	}
}

export default Layout;
