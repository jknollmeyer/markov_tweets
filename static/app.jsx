var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
              'Nov', 'Dec']

var innerCenterStyle = {
  display: "inline-block",
  position: 'relative',
  top: '40%',
  WebkitTransform: 'translateY(-50%)',
  msTransform: 'translateY(-50%)',
  transform: 'translateY(-50%)',
}
var PageHTML = React.createClass({
  getInitialState: function(){
    //Initialize the username and the fallback value
    return {username: '@', usernameOldValue: '@'};
  },
  handleUsernameChange: function(e){
    //If the user tries to change the '@', revert to the last username
    if(e.target.value.charAt(0) != '@') this.setState({username: this.state.usernameOldValue});
    //Else, update the username and the fallback value
    else{
      this.setState({username: e.target.value, usernameOldValue: e.target.value});
    }
  },
  resetTweet: function(e){
    this.setState({responseSuccess: false});
  },
  handleSubmit: function(e){
    e.preventDefault();
    this.setState({
      pageData: 'Loading...',
      loading: true,
      responseSuccess: false,
      status: '',
      twitPic: '',
      profileName: '',
      tweetTime: '',
    });
    var username = this.state.username.trim();
    if(!username){
      this.setState({pageData: "Please enter a username" });
      return;
    }

    $.ajax({
      url: "http://localhost:5000/tweets",
      type: 'POST',
      dataType: 'json',
      data: {username: username},
      success: function(data) {
        this.setState({loading: false, pageData: ''})
        //Catch a 404 from the API call, which should be caused by invalid user
        if (data == '404') this.setState({status: 'Username entered was invalid'});
        //401 Unauthorized Error
        else if (data == '401') this.setState({status: 'The selected user has a protected account'});
        //Catchall for all other HTTP errors
        else if(data == '204') this.setState({status: 'Account has no tweets to generate a model from'})
        else if(data == 'UNKNOWN') this.setState({status: 'Unknown error'});
        //Save the generated tweet text and record a successful response
        else{
          var now = new Date();
          var dateString = (" - " + now.getDate() + " " + MONTHS[now.getMonth()]
                            + " " + now.getFullYear());
          var profileURL = "https://twitter.com/" + this.state.username;
          this.setState({
            pageData: data.tweet,
            twitPic: data.pic,
            responseSuccess: true,
            loading: false,
            tweetTime: dateString,
            profileURL: profileURL,
            profileName: data.name
          });
        }
      }.bind(this),
      error: function(xhr, status, err){
        console.error(status, err.toString());
      }.bind(this)
    });
  },


  render: function(){
    var partial;
    //If we generate a tweet, partial becomes a twitter card
    if(this.state.responseSuccess || this.state.loading){
      var usernameStyle = {fontWeight: 'normal', color: '#8899a6'};
      var twitpicStyle = {borderRadius: 5, width: 48, height: 48};
      var tweetCardStyle = {textAlign: 'left', backgroundColor:'white'};
      var statusStyle = {color: 'red', fonWeight: 'bold'}
      partial = (
        <div style={innerCenterStyle}>
          <blockquote className="twitter-tweet" style={tweetCardStyle}>
            <a href={this.state.profileURL}>
               <img src={this.state.twitPic} style={twitpicStyle}/>
            </a>
            <span>&nbsp;{this.state.profileName}&nbsp;</span>
            <span style={usernameStyle}>
              {this.state.username}&nbsp;
              {this.state.tweetTime}
            </span>
            <p>{this.state.pageData}</p>
          </blockquote>
          <div>
            <button type="button" className="btn btn-default"
               onClick={this.handleSubmit}>
              Regenerate Tweet</button>
            <button type="button" className="btn btn-default"
              onClick={this.resetTweet}>
              Try a different account
            </button>
          </div>
        </div>


      )
    }else{
      partial = (
        <div style={innerCenterStyle}>
          <form className="usernameForm" onSubmit={this.handleSubmit}>
            <input
              type="text"
              placeholder="Twitter username"
              value={this.state.username}
              onChange={this.handleUsernameChange}
            />
            <input type="submit" value="Generate" />
          </form>
          <p style={statusStyle}>{this.state.status}</p>
      </div>
      )
    }

    return (
      partial
    );
  }
});


ReactDOM.render(
  <PageHTML/>,
  document.getElementById('appContainer')
);
