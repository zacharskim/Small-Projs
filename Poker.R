library(tidyverse)
library(stringr)
library(reticulate)

##########Functions For Cards################

get_deck <- function(){
  setClass("card", slots=list(rank="character", suit='character', `one below`='character'))
  
  card_list <- c()
  for(j in c('C','S','D','H')){ 
    for(i in c('A','2','3','4','5','6','7','8','9','10','J','Q','K')){
      temp <- new("card",rank=i, suit=j, `one below`='temp'  )
      card_list <- append(temp, card_list)
    }
    index <- 1
    
    
    for(i in 1:52){
      if(index < 13){
        card_list[[i]]@`one below` <- card_list[[index+1]]@rank
        index <- index + 1
      }
      
    }
    
    card_list[[13]]@`one below`  <- 'K'
    
    card_list[[13]]@`one below`  <- 'K'
    card_list[[13]]@`one below`  <- 'K'
    card_list[[13]]@`one below`  <- 'K'
  }
  return(card_list)
}

card_obj_to_string <- function(hand){
  res <- c()
  for(i in 1:length(hand)){
    temp <- paste0(deck[[i]]@rank, deck[[i]]@suit)
    res <- append(res, temp)
  }
  
  return(res)
}

#need to name the deck to have multiple decks...
deal_cards <- function(num_cards, deck, deck_name, output_type){
  
  card_index <- sample(seq_along(deck), num_cards, replace = FALSE)
  cards <- deck[card_index]
  
  
  if(output_type == 'object'){
    deck <- deck[-card_index]
    assign(deck_name, deck, env=.GlobalEnv)
    
    return(cards)
  }
  
  if(output_type == 'array'){
    
    
    card_returned <- c()
    for(i in card_index){
      temp <- paste0(deck[[i]]@rank, deck[[i]]@suit)
      card_returned <- append(card_returned, temp)
    }
    deck <- deck[-card_index]
    assign(deck_name, deck, env=.GlobalEnv)
    
    
    return(card_returned)
  } else {
    print("Enter in output_type as 'object' or 'array'")
  }
  
}

burn_card <- function(deck, deck_name, return_card){
  
  card_index <- sample(seq_along(deck), 1, replace = FALSE)
  
  return_this <- paste0(deck[[card_index]]@rank, deck[[card_index]]@suit)
  
  
  deck <- deck[-card_index]
  assign(deck_name, deck, env=.GlobalEnv)
  
  if(!missing(return_card)){
    return(return_this)
  }
}



hand_to_objs <- function(array_hand){
  hand_objs <- c()
  for(i in 1:length(array_hand)){
    if(str_detect(array_hand[i],'K')){
      temp <- new("card",rank='K', suit=substr(array_hand[i], start = nchar(array_hand[i]), stop = nchar(array_hand[i])))
      hand_objs <- append(hand_objs,temp)
      
    } else if(str_detect(array_hand[i],'Q')){
      temp <- new("card",rank='Q', suit=substr(array_hand[i], start = nchar(array_hand[i]), stop = nchar(array_hand[i])))
      hand_objs <- append(hand_objs,temp)
      
    }else  if(str_detect(array_hand[i],'J')){
      temp <- new("card",rank='J', suit=substr(array_hand[i], start = nchar(array_hand[i]), stop = nchar(array_hand[i])))
      hand_objs <- append(hand_objs,temp)
      
    }else if(str_detect(array_hand[i],'A')){
      temp <- new("card",rank='A', suit=substr(array_hand[i], start = nchar(array_hand[i]), stop = nchar(array_hand[i])))
      hand_objs <- append(hand_objs,temp)
    } else {
      temp <- new("card",rank=as.character(parse_number(array_hand[i])), suit=substr(array_hand[i], start = nchar(array_hand[i]), stop = nchar(array_hand[i])))
      hand_objs <- append(hand_objs,temp)
    }
  }
  
  
  return(hand_objs)
}



sort_card_obj_rank <- function(obj_list){
  obj_rank_num <- c()
  for(i in obj_list){
    if(!(i@rank %in% c('K','Q','J','A'))){
      obj_rank_num <- append(obj_rank_num, parse_number(i@rank))
    } else{
      if(i@rank == 'K'){
        obj_rank_num <- append(obj_rank_num, 13)
      }
      
      if(i@rank == 'Q'){
        obj_rank_num <- append(obj_rank_num, 12)
      }
      
      if(i@rank == 'J'){
        obj_rank_num <- append(obj_rank_num, 11)
      }
      
      if(i@rank == 'A'){
        obj_rank_num <- append(obj_rank_num, 14)
      }
    }
  }
  sort(obj_rank_num)
}


get_hand_suit_freq <- function(obj_list){
  suit_list <- c()
  for(i in obj_list){
    suit_list <- append(suit_list,i@suit) 
  }
  table(suit_list)
  
}


hand_identifier <- function(hand){
  
  #check if hand is two of a kind
  hand_numeric <- sort_card_obj_rank(hand)
  tbl_num <- table(hand_numeric)
  hand_output <- c()
  
  if(sum(tbl_num == 2) >= 1){
    num <- sum(tbl_num == 2)
    temp <- paste(num, 'pair')
    hand_output <- append(hand_output, temp)
  }
  
  
  #check if hand is three of a kind
  hand_numeric <- sort_card_obj_rank(hand)
  tbl_num <- table(hand_numeric)
  if(sum(tbl_num == 3) >= 1){
    num <- sum(tbl_num == 3)
    temp <- paste(num, 'three of a kind')
    hand_output <- append(hand_output, temp)
    
  }
  
  
  
  #check if hand is 4 of a kind
  hand_numeric <- sort_card_obj_rank(hand)
  tbl_num <- table(hand_numeric)
  if(sum(tbl_num >= 4) >= 1){
    num <- sum(tbl_num >= 4)
    temp <- paste(num, 'four of a kind')
    hand_output <- append(hand_output, temp)
    
  }
  
  
  #check for a straight
  links <- sum(diff(hand_numeric) == 1)
  if(links >= 4){
    hand_output <- append(hand_output, 'straight!')
  }
  
  if(14 %in% hand_numeric & (sum(hand_numeric %in% c(2,3,4,5) ) == 4)){  
    hand_output <- append(hand_output, 'ace low straight')
  }
  
  
  
  #check for a flush
  if(sum(get_hand_suit_freq(hand)>= 5) >= 1){
    temp <- 'flush'
    hand_output <- append(hand_output, temp)
    
  }
  
  max_card_val <- max(hand_numeric)
  high_card <- max_card_val
  
  if(max_card_val %in% c(11,12,13,14)){
    if(max_card_val== 11){
      high_card <- 'J'
    }else if(max_card_val == 12){
      high_card <- 'Q'
    }else if(max_card_val == 13){
      high_card <- 'K'
    }else if(max_card_val == 14){
      high_card <- 'A'
    } 
    
  }
  
  high_card_out <- paste0('high card is ', high_card)
  hand_output <- append(hand_output, high_card_out)
  return(hand_output)
  
}


###########Functions For Dealing Cards ############

first_deal <- function(){
  initial_player_hand <<- deal_cards(num_cards = 2, deck  = deck, deck_name = 'deck', output_type = 'object')
  
  initial_bot_hand <<- deal_cards(num_cards = 2, deck  = deck, deck_name = 'deck', output_type = 'object')
  return(initial_player_hand)
}

get_flop <- function() {
  burn_card(deck = deck, deck_name = 'deck')
  flop <<- deal_cards(num_cards = 3, deck  = deck, deck_name = 'deck', output_type = 'object')
  print("The flop is:")
  print(card_obj_to_string(flop))
}

get_turn <- function(){
  burn_card(deck = deck, deck_name = 'deck')
  turn <<- deal_cards(num_cards = 1, deck  = deck, deck_name = 'deck', output_type = 'object')
  print("Current Cards:")
  print(card_obj_to_string(turn))
}


get_river <- function(){
  burn_card(deck = deck, deck_name = 'deck')
  river <<-deal_cards(num_cards = 1, deck  = deck, deck_name = 'deck', output_type = 'object')
  print("River:")
  print(card_obj_to_string(river))
}

get_final_hands <- function(){
  player_hand <<- c(initial_player_hand, flop,turn,river)
  bot_hand <<- c(initial_bot_hand, flop,turn,river)
}

####Functions For Betting/Checking Etc############
bet <- function(balance, betSize, player){
  if(balance - betSize < 0){
    print('Please make sure your bet is less than your current balance!')
  } else{
    if(player == 'bot'){
      bot_balance <<- get_balance(player = 'bot') - betSize
      pot <<- pot + betSize
      return(bot_balance)
    } else {
      player_balance <<- get_balance(player = 'not bot') - betSize
      pot <<- pot + betSize
      return(player_balance)
    }
    
  }
}

bot_bet_check_call_raise_fold <- function(betOrRaisePct, callOrCheckPct){
  actions <- c("bet/raise","call/check", "fold")
  
  num <- round(100*betOrRaisePct)
  num1 <- round(100*callOrCheckPct)
  num2 <- 100 - num - num1
  action_taken <- sample(c(sample(actions[1], num, replace = TRUE), sample(actions[2], num1, replace = TRUE), sample(actions[3], num2, replace = TRUE)))
  
  action <- sample(action_taken, 1)
  
  if(action == "bet/raise"){
    botBet <<- bot_balance*sample(1:100,1)/100
    bet(bot_balance, botBet, player = 'bot')
    print('Bot decides to bet/raise')
  } else if(action == "call/check"){
    print('Bot decides to call/check')
    pot <<- pot + betAmount 
    bot_balance <<- bot_balance - betAmount
  } else {
    print('Bot decides to fold')
    playerWins <<- playerWins + 1
    poker()
    return(-1)
  }
  
}

didTheOtherBetOrRaise <- function(){
  if(betAmount != 0){
    if(bot_balance > betAmount){
      bot_balance <<- bot_balance - (betAmount - botBet)
      pot <<- pot + (betAmount - botBet)
      betAmount <<- 0
    } else {
      print('Bot decides to fold')
      playerWins <<- playerWins + 1
      poker()
      
    }
    
  }
  
  if(botBet != 0){
    print(paste("The bot just bet:",botBet))
    userChoice <- readline(prompt = "Would you like to match him? (yes or no):")
    if(userChoice == 'yes'){
      difference <- botBet - betAmount
      player_balance <<- player_balance - difference
      pot <<- pot + difference
      botBet <<- 0
      print(paste0("The new pot is ",pot))

    } else{
      print("You choose to fold")
      bot_balance <<- bot_balance + pot
      botWins <<- botWins + 1
      pot <<- 0 
      Sys.sleep(3)
      poker()
    }
  }
  
}


#### Determine Winner Functions ####

rank_hand <- function(hand){
  sum <- 0
  hand_vec <- hand_identifier(hand)
  if('1 pair' %in% hand_vec){
    sum <- sum + 15
  }
  if('2 pair' %in% hand_vec){
    sum <- sum + 16
  }
  if('3 pair' %in% hand_vec){
    sum <- sum + 17
  }
  if('1 three of a kind' %in% hand_vec){
    sum <- sum + 18
  }
  if('2 three of a kind' %in% hand_vec){
    sum <- sum + 19
  }
  if('four of a kind' %in% hand_vec){
    sum <- sum + 20
  }
  if('straight!' %in% hand_vec){
    sum <- sum + 21
  }
  
  if('flush' %in% hand_vec){
    sum <- sum + 22
  }
  
  if('1 pair' %in% hand_vec & '1 three of a kind' %in% hand_vec){
    sum <- sum + 23
  }
  
  if(str_detect(hand_vec[length(hand_vec)], 'high card is')){
    hand_numeric <- sort_card_obj_rank(hand)
    sum <- sum + max(hand_numeric)
  } 
  
  return(sum)
  
}


determine_winner <- function(){
  
  if(rank_hand(player_hand) > rank_hand(bot_hand)){
    playerWins <<- playerWins + 1
    player_balance <<- player_balance + pot
    print("Player Won with")
    print(hand_identifier(player_hand))
    pot <<- 0
  } else {
    botWins <<- botWins + 1
    print("Bot won with")
    print(bot_hand)
    bot_balance <<- bot_balance + pot
    pot <<- 0
  }
  
}

bet_call_function <- function(){
  userInput <- readline(prompt = "Please type bet, check, or fold:")
  if(userInput == 'bet'){
    betAmount <<- as.numeric(readline(prompt = 'How much would you like to bet?:'))
    bet(player_balance, betAmount, player = 'not bot')
  } else if(userInput == 'check') {
    print('You choose check/call')
    print("Bots turn now")
    Sys.sleep(3)
  } else {
    print('You choose fold')
    bot_balance <- bot_balance + pot
    botWins <<- botWins + 1
    pot <<- 0
    betAmount <<- 0
    poker()
  }
  #bot turn now
  botChoice <- bot_bet_check_call_raise_fold(.55,.45)
  if(botChoice == -1){
    player_balance <- player_balance + pot
    playerWins <<- playerWins + 1
    pot <<- 0
    betAmount <<- 0
    
  } else {
  print(paste0('The current pot is:',pot))
  }
  
}

#global variables
#playerWins,botWins, pot, bot_balance, player_balance, player_hand, pot_hand
#initial_player_hand, deck

deck <<- get_deck()
botBet <<- 0
betAmount <<- 0
pot <<- 0
playerWins <<- 0
botWins <<- 0

poker <- function(){
  while(player_balance > 0 || bot_balance > 0 ){
    print("Here are your starting Cards")
    print(card_obj_to_string(first_deal()))
    Sys.sleep(5)
    bet_call_function()
    didTheOtherBetOrRaise()
    get_flop()
    bet_call_function()
    didTheOtherBetOrRaise()
    get_turn()
    bet_call_function()
    didTheOtherBetOrRaise()
    get_river()
    bet_call_function()
    didTheOtherBetOrRaise()
    get_final_hands()
    determine_winner()
  }
}

bot_balance <- as.numeric(readline(prompt = 'Please enter the starting Balance for each player:'))
player_balance <- bot_balance
while(player_balance > 0 || bot_balance > 0 ){
  poker()
}

