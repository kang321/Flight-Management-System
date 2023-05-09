import React from "react";
import NavigationItems from "../../Navigation/NavigationItems/NavigationItems";
import classes from "./SideDrawer.module.css";
import Backdrop from "../../UI/Backdrop/Backdrop";

const sidedrawer = (props) => {
	let attachedClasses = [classes.SideDrawer, classes.Close];

	if (props.drawerStatus) {
		attachedClasses = [classes.SideDrawer, classes.Open];
	}
	return (
		<React.Fragment>
			<Backdrop show={props.drawerStatus} clicked={props.closed} />
			<div className={attachedClasses.join(" ")}>
				<nav>
					<NavigationItems />
				</nav>
			</div>
		</React.Fragment>
	);
};

export default sidedrawer;
