# Change Log
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [Unreleased]

## [1.1.0] - 2017-11-14
### changed
- Changes priority in assignation of dispensers to delivery orders of sale orders to includes dispensers recently activated.

## [1.0.1] - 2017-08-31
### changed
- Changes query to determine if dispenser has been assigned to delivery orders active. Only delivery orders that are in the states assigned and partially_available are now considered active.

## [1.0.0] - 2017-08-30
### added
- Assigns automatically a dispenser to a stock picking out generated from a sale order.
