var MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct',
              'Nov', 'Dec']

var PageHTML = React.createClass({
  getInitialState: function(){
    return {username: ''};
  },
  handleUsernameChange: function(e){
    this.setState({username: e.target.value});
  },
  resetTweet: function(e){
    this.setState({responseSuccess: false});
  },
  handleSubmit: function(e){
    e.preventDefault();
    this.setState({pageData: 'Loading...', loading: true, responseSuccess: false, status: ''});
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
        //Catch a 404 from the API call, which should be caused by invalid user
        if (data == '404') this.setState({
          status: 'Username entered was invalid',
          loading: false,
          pageData: ''
        });
        //Catchall for all other HTTP errors
        else if(data == 'UNKNOWN') this.setState({
          status: 'Unknown error',
          loading: false,
          pageData: ''
        });
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
      partial = (
        <div>
          <blockquote className="twitter-tweet">
            <a href={this.state.profileURL}>
               <img src={this.state.twitPic} style={twitpicStyle}/>
            </a>
            <span>&nbsp;{this.state.profileName}&nbsp;</span>
            <span style={usernameStyle}>
              @{this.state.username}&nbsp;
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
        <div>
          <form className="usernameForm" onSubmit={this.handleSubmit}>
            <input
              type="text"
              placeholder="Twitter username"
              value={this.state.username}
              onChange={this.handleUsernameChange}
            />
            <input type="submit" value="Generate" />
          </form>
          <p>{this.state.status}</p>
      </div>
      )
    }

    return (
      partial
    );
  }
});


ReactDOM.render(
  <PageHTML />,
  document.getElementById('twitter_login')
);
