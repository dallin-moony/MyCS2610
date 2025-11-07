function Key(props) {
    console.log(props);
    const className = props.className ? `key ${props.className}` : 'key';
    return (
        <div data-label={props.label} className={className}>
            {props.label}
        </div>
    );
}

export default Key;
