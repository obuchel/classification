<?php

    $client = new Elasticsearch\Client(['hosts'=>'10.90.0.1:9200']);
    //setting some default options
    $searchParams = []; 
    $searchParams['index'] = 'jhu_collection';
    $searchParams['type'] = 'application/json';
    // this is how you specify a query in ES
    $searchParams['body']['query']['match']['_all'] = '';
    //default sorting: _score descending (score  is a simple relevance metric)
    $searchParams['body']['sort'] = ['_score'];
    // the actual query. Results are stored in a PHP array
    $retDoc = $client->search($searchParams);
echo $retDoc;
    
?>    