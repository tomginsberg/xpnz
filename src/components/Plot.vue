<template>
  <div class="pt-[8.25rem] px-4 mb-32">
    <h1 class="text-3xl pb-3 font-bold pl-1 text-gray-800 dark:text-gray-200">
      Summary
    </h1>
  <div class="w-full bg-white rounded-lg shadow dark:bg-gray-800 p-4 md:p-6 justify-center">
    <div class="flex justify-between border-gray-200 border-b dark:border-gray-700 pb-3">
      <dl>
        <dt class="text-base font-normal text-gray-500 dark:text-gray-400 pb-1">Total Spending</dt>
        <dd class="leading-none text-3xl font-bold text-gray-900 dark:text-white">${{net}}</dd>
      </dl>
      <div>
        <span class="bg-green-100 text-green-800 text-xs font-medium inline-flex items-center px-2.5 py-1 rounded-md dark:bg-green-900 dark:text-green-300">
          <svg class="w-2.5 h-2.5 me-1.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m8.032 12 1.984 1.984 4.96-4.96m4.55 5.272.893-.893a1.984 1.984 0 0 0 0-2.806l-.893-.893a1.984 1.984 0 0 1-.581-1.403V7.04a1.984 1.984 0 0 0-1.984-1.984h-1.262a1.983 1.983 0 0 1-1.403-.581l-.893-.893a1.984 1.984 0 0 0-2.806 0l-.893.893a1.984 1.984 0 0 1-1.403.581H7.04A1.984 1.984 0 0 0 5.055 7.04v1.262c0 .527-.209 1.031-.581 1.403l-.893.893a1.984 1.984 0 0 0 0 2.806l.893.893c.372.372.581.876.581 1.403v1.262a1.984 1.984 0 0 0 1.984 1.984h1.262c.527 0 1.031.209 1.403.581l.893.893a1.984 1.984 0 0 0 2.806 0l.893-.893a1.985 1.985 0 0 1 1.403-.581h1.262a1.984 1.984 0 0 0 1.984-1.984V15.7c0-.527.209-1.031.581-1.403Z"/>
</svg>
{{numExpenses}} Items Tracked
        </span>
      </div>
    </div>

    <div class="grid grid-cols-2 py-3">
      <dl>
        <dt class="text-base font-normal text-gray-500 dark:text-gray-400 pb-1">Expense</dt>
        <dd class="leading-none text-xl font-bold text-blue-700">${{expenseTotal}}</dd>
      </dl>
      <dl>
        <dt class="text-base font-normal text-gray-500 dark:text-gray-400 pb-1">Income</dt>
        <dd class="leading-none text-xl font-bold text-green-500 dark:text-green-400">${{incomeTotal}}</dd>
      </dl>
    </div>

    <apexchart type="bar" :options="chartOptions" :series="chartSeries" />
    <div class="grid grid-cols-1 items-center border-gray-200 border-t dark:border-gray-700 justify-between">
      <div class="flex justify-between items-center pt-5">
        <button
          id="dropdownDefaultButton"
          data-dropdown-toggle="lastDaysdropdown"
          data-dropdown-placement="bottom"
          class="text-sm font-medium text-gray-500 dark:text-gray-400 hover:text-gray-900 text-center inline-flex items-center dark:hover:text-white"
          type="button">
          Last 6 months
          <svg class="w-2.5 m-2.5 ms-1.5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4"/>
          </svg>
        </button>
        <div id="lastDaysdropdown" class="z-10 hidden bg-white divide-y divide-gray-100 rounded-lg shadow w-44 dark:bg-gray-700">
            <ul class="py-2 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdownDefaultButton">
              <li>
                <a href="#" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Yesterday</a>
              </li>
              <li>
                <a href="#" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Today</a>
              </li>
              <li>
                <a href="#" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Last 7 days</a>
              </li>
              <li>
                <a href="#" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Last 30 days</a>
              </li>
              <li>
                <a href="#" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Last 90 days</a>
              </li>
              <li>
                <a href="#" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Last 6 months</a>
              </li>
              <li>
                <a href="#" class="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">Last year</a>
              </li>
            </ul>
        </div>

      </div>
    </div>
  </div>
<h1 class="mt-8 text-3xl pb-3 font-bold pl-1 text-gray-800 dark:text-gray-200">
      Members
    </h1>
    </div>
</template>

<script setup>
import {
  ref,
  onMounted,
  watch,
  computed,
  nextTick,
  reactive,
  defineProps,
} from "vue";
import { useRoute, useRouter } from "vue-router";
import { XPNZService } from "../service/XPNZService.js";

const expenseTotal = ref(0);
const incomeTotal = ref(0);
const net = ref(0);

const router = useRouter();
const expenses = ref([]);
const numExpenses = computed(() => expenses.value.length);
const route = useRoute();

function formatMonthYear(timestamp) {
  const date = new Date(timestamp);
  const options = { month: "long", year: "numeric" };
  return date.toLocaleDateString("en-US", options);
}

function getLastSixMonths() {
  const months = [];
  const now = new Date();
  for (let i = 5; i >= 0; i--) {
    const date = new Date(now.getFullYear(), now.getMonth() - i, 1);
    months.push(formatMonthYear(date));
  }
  return months;
}

function roundToTwoDecimals(num) {
  return Math.round(num * 100) / 100;
}

onMounted(async () => {
  const ledgerID = route.params.ledgerId;
  const data = await XPNZService.getTransactions(ledgerID);
  const members = await XPNZService.getActiveMembers(ledgerID);
  if (members.length === 0) {
    await router.push(`/${ledgerID}/members`);
    return;
  }
  expenses.value = data;
  expenses.value.forEach((item) => {
    item["month"] = formatMonthYear(item.date);
  });
  expenseTotal.value = expenses.value
    .filter((item) => item.expense_type === "expense")
    .reduce((acc, item) => acc + item.converted_total, 0);
  incomeTotal.value = expenses.value
    .filter((item) => item.expense_type === "income")
    .reduce((acc, item) => acc - item.converted_total, 0);
  net.value = expenseTotal.value - incomeTotal.value;

  net.value = roundToTwoDecimals(net.value);
  incomeTotal.value = roundToTwoDecimals(incomeTotal.value);
  expenseTotal.value = roundToTwoDecimals(expenseTotal.value);
  // round
  updateChart();
});

const chartOptions = ref({
  chart: {
    type: 'bar',
    height: 400,
    sparkline: {
      enabled: false,
    },
    toolbar: {
      show: false,
    }
  },
  plotOptions: {
    bar: {
      horizontal: true,
      columnWidth: "100%",
      borderRadiusApplication: "end",
      borderRadius: 6,
      dataLabels: {
        position: "top",
      },
    },
  },
  fill: {
    opacity: 1,
  },
  legend: {
    show: false,
  },
  dataLabels: {
    enabled: false,
  },
  tooltip: {
    shared: true,
    intersect: false,
    y: {
      formatter: function (val) {
        return "$ " + val;
      }
    }
  },
  xaxis: {
    categories: ['Feb', ' March', 'April', 'May', 'June', 'July'],
    labels: {
      show: true,
      style: {
        fontFamily: "Inter, sans-serif",
        cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
      },
      formatter: function(value) {
        return "$" + value
      }
    },
    axisTicks: {
      show: false,
    },
    axisBorder: {
      show: false,
    },
  },
  yaxis: {
    labels: {
      show: true,
      style: {
        fontFamily: "Inter, sans-serif",
        cssClass: 'text-xs font-normal fill-gray-500 dark:fill-gray-400'
      }
    }
  },
  grid: {
    show: true,
    strokeDashArray: 4,
    padding: {
      left: 2,
      right: 2,
      top: -20
    },
  }
});

const chartSeries = ref([
  {
    name: "Income",
    color: "#31C48D",
    data: [],
  },
  {
    name: "Expense",
    data: [],
    color: "#1A56DB",
  }
]);

const updateChart = () => {
  const lastSixMonths = getLastSixMonths();
  console.log(lastSixMonths)
  const incomeData = new Array(6).fill(0);
  const expenseData = new Array(6).fill(0);

  expenses.value.forEach((item) => {
    const monthIndex = lastSixMonths.indexOf(item.month);
    if (monthIndex !== -1) {
      if (item.expense_type === 'income') {
        incomeData[monthIndex] -= item.converted_total;
      } else if (item.expense_type === 'expense') {
        expenseData[monthIndex] += item.converted_total;
      }
    }
  });

  // chartOptions.value.xaxis.categories = lastSixMonths;
  chartSeries.value[0].data = incomeData;
  chartSeries.value[1].data = expenseData;
};
</script>

<style scoped>
/* Add your styles here */
</style>