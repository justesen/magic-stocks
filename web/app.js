angular.module("stocksApp", ['ngSanitize'])
  .controller("StocksController", function ($scope) {
    $scope.orderByField = "score";
    $scope.stocks = DATA;

    function severe(str) {
      return "<span class='severe'>" + str + "</span>";
    }

    function warn(str) {
      return "<span class='warn'>" + str + "</span>";
    }

    function good(str) {
      return "<span class='good'>" + str + "</span>";
    }

    $scope.format = (s, key) => {
      switch (key) {
        case "p_e":
          return s.p_e.toFixed(1);
        case "earnings_ev":
          return formatGrowth(s.growth_earnings) + " " + s.earnings_ev.toFixed(2);
        case "fcf_ev":
          return formatGrowth(s.growth_fcf) + " " + s.fcf_ev.toFixed(2);
        case "weighted_roce":
          return formatGrowth(s.growth_roce) + " " + s.weighted_roce.toFixed(0) + '%';
        case "weighted_roe":
          return formatGrowth(s.growth_roe) + " " + s.weighted_roe.toFixed(0) + '%';
        case "weighted_roa":
          return formatGrowth(s.growth_roa) + " " + s.weighted_roa.toFixed(0) + '%'
        case "p_b":
          if (s.p_b < 0) {
            return severe(s.p_b.toFixed(1));
          } else if (s.p_b > 8) {
            return warn(s.p_b.toFixed(1));
          }
          return s.p_b.toFixed(1);
        case "debt_to_equity":
          if (s.debt_to_equity > 3) {
            return warn(s.debt_to_equity.toFixed(1));
          } else if (s.debt_to_equity < 0.45) {
            return good(s.debt_to_equity.toFixed(1));
          }
          return s.debt_to_equity.toFixed(1);
        default:
          return s[key];
      }
    };

    formatGrowth = (growth) => {
      if (growth == 0) {
        return "";
      }
      const str = "(" + Math.round(100*growth) + "%)";
      if (growth > 0) {
        return good(str);
      }
      return warn(str);
    }
  });
